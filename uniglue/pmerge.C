#define max(A,B) ((A) > (B) ? (A) : (B))
#define min(A,B) ((A) < (B) ? (A) : (B))


#include <hdf5.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

// HDF5 prototypes

#include "extern_hdf5.h"

int CrackHierarchyFile(FILE *fptr, int *Grid, float GridLeftEdge[], float GridRightEdge[], int *PCount);
void pcol(float *x, int n, int m, FILE *log_fptr);


int main(int argc, char *argv[])
{

  hid_t       file_id, dset_id;
  hid_t       file_dsp_id;
  hid_t       mem_dsp_id;
  hid_t       mem_type_id;
  hid_t       dsp_id;
  hid_t       file_type_id;

  hid_t       m_file_id, m_dset_id;
  hid_t       m_file_dsp_id;

  hsize_t     size;
  hsize_t     m_size; 

  hsize_t     dims[4];
  hsize_t     xdims[4];
  hsize_t     maxdims[4];

  hsize_t     mem_stride, mem_count;
  hsize_t     m_file_stride, m_file_count;

  hssize_t    mem_offset;
  hssize_t    m_file_offset;

  herr_t      h5_status;
  herr_t      h5_error = -1;

  int i, j, k, m, n;
  int ii, jj, kk, ijk;
  int ndims;
  int ngrids;
  int gridcounter;
  int *ibuff;
  float *rbuff;
  double *dbuff;
  char *data[3];

  FILE *fptr;
  int NextGrid;
  int PCount;
  int TCount;
  float GridLeftEdge[3];
  float GridRightEdge[3];
  int Counts[1024];
  char pid[5];

  char *GridName;
  char *PartName;

  GridName = argv[1];
  PartName = argv[2];
  sscanf(argv[3], "%d", &ngrids);

  char *Hierarchy = new char[strlen(GridName)+10+1];
  char *DumpName = new char[strlen(GridName)+5+4+1];

  strcpy(Hierarchy,GridName);
  strcat(Hierarchy,".hierarchy");

  printf("Grid Name: %s\n", GridName);
  printf("Grid Count: %d\n", ngrids);

  TCount = 0;

  fptr = fopen(Hierarchy, "r");

  printf("Open %s\n",Hierarchy);

  for(gridcounter = 0; gridcounter < ngrids; gridcounter++)
  {

    n=gridcounter;

    PCount = 0;
    Counts[n] = 0;

    ijk = CrackHierarchyFile(fptr, &NextGrid, GridLeftEdge, GridRightEdge, &PCount);

    printf("Grid %d: %d\n", NextGrid, PCount);
    Counts[n] = PCount;
    TCount = TCount + PCount;
  }

  fclose(fptr);

  printf("Total particle count = %d\n", TCount);

//  for(gridcounter = 0; gridcounter < ngrids; gridcounter++)
//  {
//    printf("Counts[%d] = %d\n", gridcounter, Counts[gridcounter]);
//  }

  data[0] = new char[20];
  data[1] = new char[20];
  data[2] = new char[20];

  strcat(data[0],"particle_position_x");
  strcat(data[1],"particle_position_y");
  strcat(data[2],"particle_position_z");

  gridcounter = 0;
  n=gridcounter;

    sprintf(pid, "%4.4d", n+1);
    strcpy(DumpName, GridName);
    strcat(DumpName, ".grid");
    strcat(DumpName, pid);
    printf("Input file %s\n", DumpName);

  file_id = H5Fopen(DumpName, H5F_ACC_RDONLY, H5P_DEFAULT);
    assert( file_id != h5_error );
  dset_id = H5Dopen(file_id, PartName);
    assert( dset_id != h5_error );
  file_type_id = H5Dget_type(dset_id);
    assert( file_type_id != h5_error );
  h5_status = H5Dclose(dset_id);
    assert( h5_status != h5_error );
  h5_status = H5Fclose(file_id);
    assert( h5_status != h5_error );

  m_size = TCount;

  m_file_dsp_id = H5Screate_simple(1, &m_size, NULL);
    assert( m_file_dsp_id != h5_error );
  m_file_id = H5Fcreate(PartName, H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
    assert( m_file_id != h5_error );
  m_dset_id = H5Dcreate(m_file_id, PartName, file_type_id, m_file_dsp_id, H5P_DEFAULT);
    assert( m_dset_id != h5_error );

  m_file_offset = 0;

  for(gridcounter = 0; gridcounter < ngrids; gridcounter++)
  {

    n=gridcounter;

    sprintf(pid, "%4.4d", n+1);
    strcpy(DumpName, GridName);
    strcat(DumpName, ".grid");
    strcat(DumpName, pid);
    printf("Input file %s\n", DumpName);

    file_id = H5Fopen(DumpName, H5F_ACC_RDONLY, H5P_DEFAULT);

    dset_id = H5Dopen(file_id, PartName);

    file_dsp_id = H5Dget_space(dset_id);
    file_type_id = H5Dget_type(dset_id);
    ndims = H5Sget_simple_extent_dims(file_dsp_id, xdims, maxdims);

    size = 1;
    printf("Ndims %d\n",ndims);
    for ( i = 0; i < ndims; i++)
    {
      dims[i] = xdims[i];
      size = size * dims[i];
      printf("Dim %d\n", (int) xdims[i]);
    }
    printf("Size %d\n", (int) size);

    file_dsp_id = H5Screate_simple(ndims, dims, NULL);
    mem_dsp_id = H5Screate_simple(1, &size, NULL);

    if ( H5Tequal( file_type_id, H5T_IEEE_F32BE ) )
    {
      rbuff = new float[(int) size];
      mem_type_id = H5T_NATIVE_FLOAT;
      h5_status = H5Dread(dset_id, mem_type_id, mem_dsp_id, file_dsp_id, H5P_DEFAULT, rbuff);
        assert( h5_status != h5_error );
      printf("float read status %d\n", (int) h5_status);
    }

    if ( H5Tequal( file_type_id, H5T_IEEE_F64BE ) )
    {
      dbuff = new double[(int) size];
      mem_type_id = H5T_NATIVE_DOUBLE;
      h5_status = H5Dread(dset_id, mem_type_id, mem_dsp_id, file_dsp_id, H5P_DEFAULT, dbuff);
        assert( h5_status != h5_error );
      printf("double read status %d\n", (int) h5_status);
    }

    if ( H5Tequal( file_type_id, H5T_STD_I32BE ) )
    {
      ibuff = new int[(int) size];
      mem_type_id = H5T_NATIVE_INT;
      h5_status = H5Dread(dset_id, mem_type_id, mem_dsp_id, file_dsp_id, H5P_DEFAULT, ibuff);
        assert( h5_status != h5_error );
      printf("int read status %d\n", (int) h5_status);
    }

    h5_status = H5Sclose(file_dsp_id);
    h5_status = H5Dclose(dset_id);
    h5_status = H5Fclose(file_id);

    m_file_stride = 1;
    m_file_count = Counts[n];

    mem_offset = 0;
    mem_stride = 1;
    mem_count = size;

    h5_status = H5Sselect_hyperslab(mem_dsp_id, H5S_SELECT_SET, &mem_offset, &mem_stride, &mem_count, NULL);
      assert( h5_status != h5_error );
    h5_status = H5Sselect_hyperslab(m_file_dsp_id, H5S_SELECT_SET, &m_file_offset, &m_file_stride, &m_file_count, NULL);
      assert( h5_status != h5_error );

    if ( H5Tequal( file_type_id, H5T_IEEE_F32BE ) )
    {
      h5_status = H5Dwrite(m_dset_id, mem_type_id, mem_dsp_id, m_file_dsp_id, H5P_DEFAULT, rbuff);
        assert( h5_status != h5_error );
      delete rbuff;
    }

    if ( H5Tequal( file_type_id, H5T_IEEE_F64BE ) )
    {
      h5_status = H5Dwrite(m_dset_id, mem_type_id, mem_dsp_id, m_file_dsp_id, H5P_DEFAULT, dbuff);
        assert( h5_status != h5_error );
      delete dbuff;
    }

    if ( H5Tequal( file_type_id, H5T_STD_I32BE ) )
    {
      h5_status = H5Dwrite(m_dset_id, mem_type_id, mem_dsp_id, m_file_dsp_id, H5P_DEFAULT, ibuff);
        assert( h5_status != h5_error );
      delete ibuff;
    }

    m_file_offset = m_file_offset + m_file_count;

    h5_status = H5Sclose(mem_dsp_id);

  }

  h5_status = H5Sclose(m_file_dsp_id);
    assert( h5_status != h5_error );
  h5_status = H5Dclose(m_dset_id);
    assert( h5_status != h5_error );
  h5_status = H5Fclose(m_file_id);
    assert( h5_status != h5_error );

}



void pcol(float *x, int n, int m, FILE *log_fptr)
{

int nrow,mrow;
int i,j;

  int         io_log = 1;

if (io_log)
{
  nrow = n/m;
  mrow = n - nrow * m;
  if( mrow > 0 )
  {
    nrow = nrow+1;
  }

  fprintf(log_fptr,"\n");

  for(j=0;j<n;j=j+m)
  {
    for(i=j;i<min(j+m,n);i++)
    {
      fprintf(log_fptr, "%8.1e", x[i]);
    }
    fprintf(log_fptr,"\n");
  }
}

}
