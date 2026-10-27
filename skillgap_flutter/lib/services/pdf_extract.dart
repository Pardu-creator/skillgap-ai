import 'dart:io';
import 'dart:typed_data';

/// Best-effort pure-Dart PDF text extractor.
///
/// Handles the common case of text-based PDFs whose page content streams are
/// FlateDecode-compressed: it finds `stream...endstream` blocks, tries zlib
/// decompression, then pulls literal strings out of Tj / TJ text operators.
/// Falls back to raw byte scanning for uncompressed streams.
class PdfTextExtractor {
  static String extract(Uint8List bytes) {
    final out = StringBuffer();

    for (final streamBytes in _streamBlocks(bytes)) {
      Uint8List data = streamBytes;
      // Try FlateDecode (zlib); if it fails, scan raw bytes anyway.
      try {
        data = Uint8List.fromList(zlib.decode(streamBytes));
      } catch (_) {}
      out.write(_extractTextOps(data));
    }

    var text = out.toString();
    text = text
        .replaceAll('\\(', '(')
        .replaceAll('\\)', ')')
        .replaceAll('\\\\', '\\')
        .replaceAll(RegExp(r'[ \t]+'), ' ')
        .replaceAll(RegExp(r'\n{3,}'), '\n\n');
    return text.trim();
  }

  /// Locates all `stream`/`endstream` blocks in the file.
  static List<Uint8List> _streamBlocks(Uint8List bytes) {
    final results = <Uint8List>[];
    const marker = 'stream';
    const endMarker = 'endstream';
    int i = 0;
    while (i < bytes.length - marker.length) {
      if (_matchesAt(bytes, marker, i)) {
        int start = i + marker.length;
        // Skip CRLF / LF after 'stream'
        if (start < bytes.length &&
            bytes[start] == 0x0D &&
            bytes[start + 1] == 0x0A) {
          start += 2;
        } else if (start < bytes.length && bytes[start] == 0x0A) {
          start += 1;
        }
        int end = _indexOf(bytes, endMarker, start);
        if (end == -1) break;
        results.add(bytes.sublist(start, end));
        i = end + endMarker.length;
      } else {
        i++;
      }
    }
    return results;
  }

  static bool _matchesAt(Uint8List b, String s, int pos) {
    for (var j = 0; j < s.length; j++) {
      if (b[pos + j] != s.codeUnitAt(j)) return false;
    }
    return true;
  }

  static int _indexOf(Uint8List b, String s, int from) {
    for (var i = from; i <= b.length - s.length; i++) {
      if (_matchesAt(b, s, i)) return i;
    }
    return -1;
  }

  /// Extracts strings shown by Tj/TJ/'/" operators from a content stream.
  static String _extractTextOps(Uint8List data) {
    final out = StringBuffer();
    int i = 0;
    while (i < data.length) {
      final c = data[i];
      if (c == 0x28 /* ( */) {
        // literal string — read balanced parens
        final buf = StringBuffer();
        int depth = 1;
        i++;
        while (i < data.length && depth > 0) {
          final ch = data[i];
          if (ch == 0x5C /* \ */ && i + 1 < data.length) {
            buf.writeCharCode(data[i + 1]);
            i += 2;
            continue;
          }
          if (ch == 0x28) depth++;
          if (ch == 0x29) depth--;
          if (depth > 0) buf.writeCharCode(ch);
          i++;
        }
        out.write(buf.toString());
      } else if (c == 0x54 /* T */ && i + 1 < data.length) {
        // Tj / TD / T* → line break hint
        out.write('\n');
        i++;
      } else {
        i++;
      }
    }
    return out.toString();
  }

  /// Convenience: extract from a file path (desktop) or bytes.
  static Future<String> extractFromPath(String path) async {
    final bytes = await File(path).readAsBytes();
    return extract(bytes);
  }
}
