# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class NavMeshPath(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsNavMeshPath(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = NavMeshPath()
        x.Init(buf, n + offset)
        return x

    # NavMeshPath
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # NavMeshPath
    def Path(self, j):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(tdw.flatbuffers.number_types.Uint8Flags, a + tdw.flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # NavMeshPath
    def PathAsNumpy(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(tdw.flatbuffers.number_types.Uint8Flags, o)
        return 0

    # NavMeshPath
    def PathLength(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # NavMeshPath
    def State(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 1

    # NavMeshPath
    def Id(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def NavMeshPathStart(builder): builder.StartObject(3)
def NavMeshPathAddPath(builder, path): builder.PrependUOffsetTRelativeSlot(0, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(path), 0)
def NavMeshPathStartPathVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def NavMeshPathAddState(builder, state): builder.PrependUint8Slot(1, state, 1)
def NavMeshPathAddId(builder, id): builder.PrependInt32Slot(2, id, 0)
def NavMeshPathEnd(builder): return builder.EndObject()
