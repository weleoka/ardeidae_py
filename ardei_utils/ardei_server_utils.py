import tempfile
"""
Here are some functions reqired for the ardeidae_py servers to run.
"""


"""
Make a named temporary file and fill it with chars.
parameters:
    ri: The recieved integer from client.

returns temporaryfile instance.
"""
def make_file(ri):
    tf = tempfile.NamedTemporaryFile()
    chunkStr = 'A'
    for x in range(0, ri):
        chunk = chunkStr.encode('utf-8')
        tf.write(chunk)

    tf.flush() # Flush the write buffer to file.
    return tf