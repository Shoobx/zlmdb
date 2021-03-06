# automatically generated by the FlatBuffers compiler, do not modify

# namespace: accelstorage

import flatbuffers

# /// A series of samples from the accelerometer sensor.
class AccelSeries(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsAccelSeries(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = AccelSeries()
        x.Init(buf, n + offset)
        return x

    # AccelSeries
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

# /// Unix epoch when sample batch was recorded (start thereof).
    # AccelSeries
    def SampleStart(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

# /// Sample length in ms.
    # AccelSeries
    def SamplePeriod(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, o + self._tab.Pos)
        return 0

# /// Sample batch with accelerometer readings.
    # AccelSeries
    def Samples(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 12
            from .AccelSample import AccelSample
            obj = AccelSample()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # AccelSeries
    def SamplesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def AccelSeriesStart(builder): builder.StartObject(3)
def AccelSeriesAddSampleStart(builder, sampleStart): builder.PrependUint64Slot(0, sampleStart, 0)
def AccelSeriesAddSamplePeriod(builder, samplePeriod): builder.PrependUint16Slot(1, samplePeriod, 0)
def AccelSeriesAddSamples(builder, samples): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(samples), 0)
def AccelSeriesStartSamplesVector(builder, numElems): return builder.StartVector(12, numElems, 4)
def AccelSeriesEnd(builder): return builder.EndObject()
