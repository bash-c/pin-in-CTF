#include "pin.H"
#include <fstream>
 
std::ofstream TraceFile;
PIN_LOCK lock;
ADDRINT main_begin;
ADDRINT main_end;
 
static ADDRINT WriteAddr;
static INT32 WriteSize;
 
static VOID RecordWriteAddrSize(ADDRINT addr, INT32 size)
{
    WriteAddr = addr;
    WriteSize = size;
}
 
static VOID RecordMemWrite(ADDRINT ip)
{
    UINT8 memdump[256];
    PIN_GetLock(&lock, ip);
    PIN_SafeCopy(memdump, (void *)WriteAddr, WriteSize);
    if (WriteSize==1)
        TraceFile << static_cast<CHAR>(*memdump);
    PIN_ReleaseLock(&lock);
}
 
VOID Instruction_cb(INS ins, VOID *v)
{
    ADDRINT ip = INS_Address(ins);
    if ((ip < main_begin) || (ip > main_end))
        return;
 
    if (INS_IsMemoryWrite(ins))
    {
        INS_InsertPredicatedCall(
            ins, IPOINT_BEFORE, (AFUNPTR)RecordWriteAddrSize,
            IARG_MEMORYWRITE_EA,
            IARG_MEMORYWRITE_SIZE,
            IARG_END);
        if (INS_HasFallThrough(ins))
        {
            INS_InsertCall(
                ins, IPOINT_AFTER, (AFUNPTR)RecordMemWrite,
                IARG_INST_PTR,
                IARG_END);
        }
    }
}
 
void ImageLoad_cb(IMG Img, void *v)
{
    PIN_GetLock(&lock, 0);
    if(IMG_IsMainExecutable(Img))
    {
        main_begin = IMG_LowAddress(Img);
        main_end = IMG_HighAddress(Img);
    }
    PIN_ReleaseLock(&lock);
}
 
VOID Fini(INT32 code, VOID *v)
{
    TraceFile.close();
}
 
int  main(int argc, char *argv[])
{
    PIN_InitSymbols();
    PIN_Init(argc,argv);
    TraceFile.open("trace-1byte-writes.bin");
    if(TraceFile == NULL)
        return -1;
    IMG_AddInstrumentFunction(ImageLoad_cb, 0);
    INS_AddInstrumentFunction(Instruction_cb, 0);
    PIN_AddFiniFunction(Fini, 0);
    PIN_StartProgram();
    return 0;
}
