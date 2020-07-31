int fgetpos(FILE *stream)
{
    count = 0;
    while (TRUE)
    {
        BYTE b;
        fread(&b, 1, 1, stream);
        if (feof(stream))
        {
            break;
        }
        count++;
    }
    return stream->size - count;
}

bool fsetpos(FILE *stream, int offset)
{
    if (offset > size || offset < 0)
    {
     return FALSE
    }
    count = 0;
    for (i = 0; i < offset; i++)
    {
        BYTE b;
        fread(&b, 1, 1, stream);
        if (feof(stream))
        {
            break;
        }
    }
    return TRUE;
}

typedef unsigned char BYTE;

bool fwrite(BYTE *buffer, int size, FILE *stream)
{
    for (i = 0; i < size; i++)
    {
     stream->current_byte = *buffer
     BYTE b;
        fread(&b, 1, 1, stream);
        if (feof(stream))
        {
            break;
        }
    }
    count = 0;
    while (TRUE)
    {
     BYTE b;
        fread(&b, 1, 1, stream);
        if (feof(stream))
        {
            break;
        }
        count++;
    }
    stream->size = count
    return TRUE;
}

bool feof(FILE *stream)
{
    if (stream->current_byte = EOF)
    {
     return TRUE;
    }
    else
    {
     return FALSE;
    }
}