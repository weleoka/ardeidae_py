import tempfile

def make_file(ri):
    tf = tempfile.NamedTemporaryFile()
    chunkStr = 'A'
    for x in range(0, ri):
        chunk = chunkStr.encode('utf-8')
        tf.write(chunk)

    tf.flush() # Flush the write buffer to file.
    return tf