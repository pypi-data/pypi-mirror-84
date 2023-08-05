// ----------------------------------------------------------------------------
//  PyAOgmaNeo
//  Copyright(c) 2020 Ogma Intelligent Systems Corp. All rights reserved.
//
//  This copy of PyAOgmaNeo is licensed to you under the terms described
//  in the PYAOGMANEO_LICENSE.md file included in this distribution.
// ----------------------------------------------------------------------------

#include "PyHelpers.h"

using namespace pyaon;

void StreamReader::read(void* data, int len) {
    ins.read(static_cast<char*>(data), len);
}

void StreamWriter::write(const void* data, int len) {
    outs.write(static_cast<const char*>(data), len);
}

void BufferReader::read(void* data, int len) {
    for (int i = 0; i < len; i++)
        static_cast<unsigned char*>(data)[i] = (*buffer)[start + i];

    start += len;
}

void BufferWriter::write(const void* data, int len) {
    int start = buffer.size();

    buffer.resize(buffer.size() + len);

    for (int i = 0; i < len; i++)
        buffer[start + i] = static_cast<const unsigned char*>(data)[i];
}
