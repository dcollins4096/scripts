//
// A more variable version of the hierarchy parser.
// The only assumption is that the info start with "Grid = X" and ends with a blank line.
// and that array lengths come sometime before the array.
//
// Only queries GridLeft and Right Edge, Pcount, and NextGrid, though other 
// fields are defined.
// This make the 4th hierarchy parser I've written.  I love doing this, its awesome.
// 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NOFAIL 0
#define FAIL -1
#define PSYM "f"
#define FSYM "f"

int ReadListOfInts(FILE *fptr, int N, int nums[]);
int ReadListOfFloats(FILE *fptr, int N, float floats[]);

void ReadIntsFromString(char * string,  int size_of_array,int * array){
  char * pointer = string;
  for( int counter = 0;  counter < size_of_array  ; counter++)
    array[counter] =  strtol(pointer, &pointer,0);
}
void ReadFloatsFromString(char * string, int size_of_array,float * array){
  char * pointer = string;
  for( int counter = 0;  counter < size_of_array  ; counter++)
    array[counter] =  strtod(pointer, &pointer);
}
int CrackHierarchyFile(FILE *fptr, int *GridIn, float GridLeftEdge[], float GridRightEdge[], int *PCount)
{

int Grid;
int ThisGrid, NextGrid;
int GridRank;
int GridDimension[3];
int GridStartIndex[3];
int GridEndIndex[3];
//float GridLeftEdge[3];
//float GridRightEdge[3];
float Time;
int SubgridsAreStatic;
int NumberOfBaryonFields;
int FieldType[16];
char *BaryonFileName;
float CourantSafetyNumber;
int PPMFlatteningParameter;
int PPMDiffusionParameter;
int PPMSteepeningParameter;
int NumberOfParticles;
char *ParticleFileName;
int GravityBoundaryType;
int SelfGravity;

 BaryonFileName = new char[101];
 ParticleFileName = new char[101];
#define MAX_LINE_LENGTH 512
 char line[MAX_LINE_LENGTH];
 char * newline = "\n";
 //Get the grid id.
 do{
   if( fgets(line, MAX_LINE_LENGTH, fptr) == NULL )
     return 0;
 }while(sscanf(line, "Grid = %d\n", &Grid) != 1);
 
 int GridBool = 0, LeftEdgeBool = 0, RightEdgeBool = 0, NextGridBool=0, PcountBool=0;
 //Read the other stuff.
 do{
   if( fgets(line, MAX_LINE_LENGTH, fptr) == NULL )
     return 0;

   GridBool += sscanf(line, "GridRank = %d\n", &GridRank);

   if( GridBool != 0 ){
     if( strstr(line, "GridLeftEdge") != NULL ){
       ReadFloatsFromString( strstr(line,"=") +1, GridRank,GridLeftEdge);
       LeftEdgeBool++;
     }
     
     if( strstr(line, "GridRightEdge") != NULL ){
       ReadFloatsFromString( strstr(line,"=") +1, GridRank,GridRightEdge);
       RightEdgeBool++;
     }
   }//grid bool.

   PcountBool += sscanf(line, "NumberOfParticles = %d\n", &PCount);
   NextGridBool +=sscanf(line, "Pointer: Grid[%d]->NextGridThisLevel = %d\n", &ThisGrid, &GridIn);   

 }while( strstr(line,newline) != line );

 if( GridBool == 0 )
   {fprintf(stderr, "error reading grid\n"); return FAIL;}
 if( LeftEdgeBool == 0 )
   {fprintf(stderr, "error reading LeftEdge\n"); return FAIL;}
 if( RightEdgeBool == 0 )
   {fprintf(stderr, "error reading RightEdge\n"); return FAIL;}
 if( PcountBool == 0 )
   {fprintf(stderr, "error reading Pcount\n"); return FAIL;}
 if( NextGridBool == 0 )
   {fprintf(stderr, "error reading NextGrid\n"); return FAIL;}

  return NOFAIL;

}



// ListIO.C


/***********************************************************************
/
/  READ/WRITE LIST OF INTS/FLOATS
/
/  written by: Greg Bryan
/  date:       November, 1994
/  modified1:
/
/  PURPOSE:
/
************************************************************************/

#include <stdio.h>

#ifdef FAIL
#undef FAIL
#endif
#define FAIL      0
#define SUCCESS   1



int ReadListOfInts(FILE *fptr, int N, int nums[])
{
  for (int i = 0; i < N; i++)
    if (fscanf(fptr, "%d", nums + i) != 1)
      return FAIL;

  fscanf(fptr, "\n");
  return SUCCESS;
}

void WriteListOfInts(FILE *fptr, int N, int nums[])
{
  for (int i = 0; i < N; i++)
    fprintf(fptr, "%d ", nums[i]);
  fprintf(fptr, "\n");
}

int ReadListOfFloats(FILE *fptr, int N, float floats[])
{
  for (int i = 0; i < N; i++)
    if (fscanf(fptr, "%f", floats + i) != 1)
      return FAIL;

  fscanf(fptr, "\n");
  return SUCCESS;
}

void WriteListOfFloats(FILE *fptr, int N, float floats[])
{
  for (int i = 0; i < N; i++)
    fprintf(fptr, "%.7g ", floats[i]);
  fprintf(fptr, "\n");
}


void WriteListOfFloats(FILE *fptr, int N, double floats[])
{
  for (int i = 0; i < N; i++)
    fprintf(fptr, "%.14g ", floats[i]);
  fprintf(fptr, "\n");
}

int ReadListOfFloats(FILE *fptr, int N, double floats[])
{
  for (int i = 0; i < N; i++)
    if (fscanf(fptr, "%lf", floats + i) != 1)
      return FAIL;

  fscanf(fptr, "\n");
  return SUCCESS;
}

void WriteListOfFloats(FILE *fptr, int N, long double floats[])
{
  for (int i = 0; i < N; i++)
    fprintf(fptr, "%.21Lg ", floats[i]);
  fprintf(fptr, "\n");
}

int ReadListOfFloats(FILE *fptr, int N, long double floats[])
{
  for (int i = 0; i < N; i++)
    if (fscanf(fptr, "%Lf", floats + i) != 1)
      return FAIL;

  fscanf(fptr, "\n");
  return SUCCESS;

}
