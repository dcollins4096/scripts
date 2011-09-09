/* 
 *   For manipulating hdf5 Enzo sets of the "cosmology restart" form.
 *   Yup.  It's spaghetti.  Suck it.
 *
 *   What things are:
 *     DataIn, DataOut: [i,j,k,3] arrays for the driving fields.  
 *   Things to change:
 *     WhatToDo:   The routine to call.
 *     SET_ID_IN:  the file name and data set name for the input
 *     SET_ID_OUT: the file name and data set name for the output
 *     DimsIn[4]:  {i,j,k,dim}
 *     DimsOut[4]: {i,j,k,dim}
 *     Add the routine to the switch.
 *   Existing routines:
 *     StupidOut:  Output[i,j,k] = i + 100 j (or something like that.)
 *     Rotate:     Rotates cube about n=[1,1,1] axis.
 *     Resize:     Sub samples.  Poor name, sorry.
 *     Nothing:    Attaches the necessary (and really redundant) attributes to the file.
 *     Sine:       Sine wave perturbation over the box.  
 *     .
 *   .
 */

#include <math.h>
#include <iostream>
#include <assert.h>
#include "hdf5.h"
//#include "extern_hdf5.h"
#include "macros_and_parameters.h"

#define MAX_DIMENSION_IN 4
#define floatdcc double
#define PI 3.14159265

#define hssize_t hsize_t

void Sine(floatdcc * Out, hsize_t* OutDims, int OutRank){

  int i, iOut, jOut, kOut, lOut, iIn, jIn, kIn, lIn, sizeIn=1, sizeOut = 1;
  int indexOut;

  //zero output field. 

  for(i=0;i<OutRank; i++)
    sizeOut*=OutDims[i];

  for(lOut=0; lOut<OutDims[3]; lOut++)
    for(kOut=0; kOut<OutDims[2]; kOut++)
      for(jOut=0;jOut<OutDims[1]; jOut++)
	for(iOut=0; iOut<OutDims[0]; iOut++){
	  indexOut=iOut + OutDims[0]*( jOut + OutDims[1] * (kOut + OutDims[2]*lOut ));
	  Out[indexOut]= sin( 3.0 );
	}
  
}

void StupidOut(floatdcc * In,  hsize_t* InDims, int InRank,
		floatdcc * Out, hsize_t* OutDims, int OutRank){

  int i, iOut, jOut, kOut, lOut, iIn, jIn, kIn, lIn, sizeIn=1, sizeOut = 1;
  int indexOut;

  for(i=0;i<OutRank; i++)
    sizeOut*=OutDims[i];

  for(lOut=0; lOut<OutDims[3]; lOut++)
    for(kOut=0; kOut<OutDims[2]; kOut++)
      for(jOut=0;jOut<OutDims[1]; jOut++)
	for(iOut=0; iOut<OutDims[0]; iOut++){
	  indexOut=iOut + OutDims[0]*( jOut + OutDims[1] * (kOut + OutDims[2]*lOut ));
	  Out[indexOut]=jOut+100*(lOut+1);
	}  
}

void Rotate(floatdcc * In,  hsize_t* InDims, int InRank,
		floatdcc * Out, hsize_t* OutDims, int OutRank){
  int i,j,k,dimO, dimI;
  int indexIn, indexOut;
  
  for(dimO=0;dimO<OutDims[3];dimO++){
    dimI = ( (0 == dimO ) ? 1 : ( ( 1 == dimO )? 2 : 0 ) );

    fprintf(stderr,"suka: dimOut %d dimIn %d \n", dimO, dimI);
    for(k=0;k<OutDims[2];k++)
      for(j=0;j<OutDims[1];j++)
	for(i=0;i<OutDims[0]; i++)
	  {
	    
	    indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	    indexIn  = k + OutDims[0]*(i + OutDims[1]*(j+ OutDims[2] * dimI));
	    Out[indexOut] = In[indexIn];
	  }
  }

}

//Sub samples the data by averaging.

void Resize(floatdcc * In,  hsize_t* InDims, int InRank,
		floatdcc * Out, hsize_t* OutDims, int OutRank){


  int Ratio = 2;// InDims[0]/OutDims[0];
  int i, iOut, jOut, kOut, lOut, iIn, jIn, kIn, lIn, sizeIn=1, sizeOut = 1;
  int indexIn, indexOut;
  int written = FALSE;

  //zero output field. 
  for(i=0;i<OutRank; i++)
    sizeOut*=OutDims[i];
  for(i=0;i<sizeOut; i++)
    Out[i]=0;

  //Do the sub-sampling.
  for(lIn=0; lIn<InDims[3]; lIn++)
    for(kIn=0; kIn<InDims[2]; kIn++)
      for(jIn=0;jIn<InDims[1]; jIn++)
	for(iIn=0; iIn<InDims[0]; iIn++){
	  
	  iOut = iIn/Ratio;
	  jOut = jIn/Ratio;
	  kOut = kIn/Ratio;
	  lOut = lIn;//NOT getting subsampled, this is vector index.
	  indexOut=iOut + OutDims[0]*( jOut + OutDims[1] * (kOut + OutDims[2]*lOut ));
	  indexIn =iIn  + InDims[0]*( jIn + InDims[1] * (kIn + InDims[2]*lIn ) );
	  
	  Out[indexOut] += In[indexIn]/(Ratio*Ratio*Ratio);
	  
	}
}

//PPML subsample.  
int PPML_SubSample(floatdcc * In,  hsize_t* InDims, int InRank,
		   floatdcc * Out, hsize_t* OutDims, int OutRank,
		   int PPML_PartToDo){

  int i,j,k,dimO = 0, dimI = PPML_PartToDo;
  int I,J,K;
  int indexIn, indexOut;
  fprintf(stderr,"Joy!\n");
  //Loop over small set, grab data from the big set.
  for(k=0;k<OutDims[2];k++)
    for(j=0;j<OutDims[1];j++)
      for(i=0;i<OutDims[0]; i++)
	{

	  //centered
	  dimO = 0;
	  I = 2*i+1;
	  J = 2*j+1;
	  K = 2*k+1;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //X_L
	  dimO = 1;
	  I = 2*i;
	  J = 2*j+1;
	  K = 2*k+1;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //X_R
	  dimO = 2;
	  I = ( (i == OutDims[0] -1 ) ? 0 : 2*i+2 ); //periodic wrap.
	  J = 2*j+1;
	  K = 2*k+1;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //Y_L
	  dimO = 3;
	  I = 2*i+1;
	  J = 2*j;
	  K = 2*k+1;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //Y_R
	  dimO = 4;
	  I = 2*i+1;
	  J = ( (j == OutDims[1] -1 ) ? 0 : 2*j+2 );
	  K = 2*k+1;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //Z_L
	  dimO = 5;
	  I = 2*i+1;
	  J = 2*j+1;
	  K = 2*k;
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	  //Z_R
	  dimO = 6;
	  I = 2*i+1;
	  J = 2*j+1;
	  K = ( ( k == OutDims[2] -1 ) ? 0 : 2*k+2);
	  indexOut = i + OutDims[0]*(j + OutDims[1]*(k+ OutDims[2] * dimO));
	  indexIn  = I + InDims[0]*(J + InDims[1]*(K+ InDims[2] * dimI));
	  Out[indexOut] = In[indexIn];
	}
}
//takes SET_ID_IN and subsamples it by 2 to SET_ID_OUT
//To use:
//Change SET_ID's to the appropriate value
//change FILE1 and FILE2
//DimsIn, slightly lower.
main() {

  //
  // Definitions.  Ignore.
  //

  hid_t       file_id, attr_dsp_id, attr_id, dataset_id, dataspace_id, float_type_id;
  herr_t      status, h5_status, h5_error = -1;

  hsize_t DimsIn[MAX_DIMENSION_IN], DimsOut[MAX_DIMENSION_IN], DimsInv[MAX_DIMENSION_IN];
  hsize_t attr_count;
  int ComponentRankIn, ComponentRankOut;
  int FieldRankIn, FieldRankOut;
  int SetRankIn, SetRankOut;
  int i, j, k, sizeIn=1, sizeOut=1;
  int Read=-1, Write=-1, WhatToDo;

  int component_rank_attr=1, component_size_attr=1, field_rank_attr, field_dims_attr[3];
  char * FILE1, * FILE2, *SET_ID_IN, *SET_ID_OUT;
  floatdcc *DataIn = NULL, *DataOut = NULL;

  //
  //function specific variables.  Make these default to something that will fail.
  //

  //for ppml sub sampling.
  int PPML_PartToDo = -1;

  //
  // Things to change! 
  //
  
  Read= TRUE;
  Write = TRUE;
  //More things to change after that 
  WhatToDo =5;//1=test output, 0=subsample 2=rotate 3=attach attribs 4=sine wave test file
              //5=ppml Left and right generation.  
  //Because Enzo is stupid, Set ID and Filename must be the same.
  SET_ID_IN  = "alexei.128.datH5";
  SET_ID_OUT = "PPML_64_VZ.h5";
  FILE1=SET_ID_IN;
  FILE2=SET_ID_OUT;

  //Component ranks (i.e. how many fields: vx,vy,vz? just vx?)
  //Field Ranks (3d, 2d, etc) 
  //And set rank (for the actual data structure.);
  ComponentRankIn  = 3;
  ComponentRankOut = 7;
  FieldRankIn = 3; 
  FieldRankOut = 3;
  SetRankIn = 4;
  SetRankOut = 4;
  //Hey!  All our datasets are fortran style, so make this shit backwards.
  DimsIn[0] = 128;
  DimsIn[1] = 128;
  DimsIn[2] = 128;
  DimsIn[3] = ComponentRankIn;

  DimsOut[0]=64;
  DimsOut[1]=64;
  DimsOut[2]=64;
  DimsOut[3]= ComponentRankOut;

  // Problem specific definitions.
  PPML_PartToDo = 2;

  fprintf(stderr,"Input file: %s Output File %s\n",SET_ID_IN,SET_ID_OUT );

  //
  //Compute size, allocate arrays
  //Don't need to touch this.
  //

  sizeIn=1;
  for(i=0;i<SetRankIn; i++)
    sizeIn*=DimsIn[i];
  
  sizeOut=1;
  for(i=0;i<SetRankOut; i++)
    sizeOut*=DimsOut[i];

  DataIn = new floatdcc[sizeIn];
  if( WhatToDo != 3 ) {
    DataOut = new floatdcc[sizeOut];
  }else{
    DataOut = DataIn;
  }

  fprintf(stderr," DataIn : %p, size = %d\n", DataIn, sizeIn);
  fprintf(stderr," DataOut: %p, size = %d sizeof = %d\n", DataOut, sizeOut, sizeof(DataOut));

  //Error check.
  if( DataIn == 0  ){
    fprintf(stderr,"Allocation for DataIn failed\n");
    return 0;
  }
  if( DataOut == 0  ){
    fprintf(stderr,"Allocation for DataOut failed\n");
    return 0;
  }
    
  int jj = sizeof(floatdcc);

  switch(jj)
    {

    case 0:float_type_id = H5T_NATIVE_INT; break;

    case 4:float_type_id = HDF5_R4;break;

    case 8:float_type_id = HDF5_R8;break;
      
    case 16:float_type_id = HDF5_R16;break;
      
    default:printf("INCORRECT FLOAT DEFINITION\n");
    }
  
  if( Read == -1 )
    fprintf(stderr,"Please define Read either TRUE or FALSE.\n");

  if( Read==TRUE){
    fprintf(stderr,"Read file %s\n",FILE1);

    //Open an existing file.
    //                name,   access mode, access properties
    file_id = H5Fopen(FILE1, H5F_ACC_RDONLY, H5P_DEFAULT);//H5F_ACC_TRUNC, H5P_DEFAULT);
    assert( file_id != h5_error );

    for(int moo=0;moo<SetRankIn;moo++)
      DimsInv[moo]=DimsIn[SetRankIn-moo-1];

    //Create data space
    dataspace_id=H5Screate_simple(SetRankIn, DimsInv, NULL);
    assert( dataspace_id != h5_error );    

    //Open dataset
    //                     duh      duh
    dataset_id = H5Dopen(file_id, SET_ID_IN);
    assert( dataset_id != h5_error);
    fprintf(stderr,"dataset opened.\n");
    fprintf(stderr,"Reading dataset.\n");
    //Read that shit.
    //               duh, memory type, mem. space, file space, transfer, data.)
    status = H5Dread(dataset_id, float_type_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, 
		     DataIn);
    assert( status != h5_error);
    fprintf(stderr,"File read.\n");
    
    //Clean up
    status = H5Sclose(dataspace_id);
    status = H5Dclose(dataset_id);
    status = H5Fclose(file_id);
  }//read

  //
  // now do something with that file
  //

  switch( WhatToDo ){
  case 0:
    fprintf(stderr,"Manipulate\n");
    Resize(DataIn, DimsIn, FieldRankIn, DataOut, DimsOut, FieldRankOut);
    break;
  case 1:
    fprintf(stderr,"Stupid Games\n");
    StupidOut(DataIn, DimsIn, FieldRankIn, DataOut, DimsOut, FieldRankOut);
    break;
  case 2:
    Rotate(DataIn, DimsIn, FieldRankIn, DataOut, DimsOut, FieldRankOut);
    break;
  case 3:
    //I just re-assigned the pointer above, so we're pretty much set.
    break;
  case 4:
    Sine(DataOut, DimsOut, FieldRankOut);
    break;
  case 5:
    PPML_SubSample(DataIn, DimsIn, FieldRankIn, DataOut, DimsOut, FieldRankOut, PPML_PartToDo);
    break;
  }

  if( Write == -1 )
    fprintf(stderr,"Please define Write either TRUE or FALSE.\n");

  if( Write == TRUE){

    //Create File

    fprintf(stderr,"Create output file %s\n",FILE2);
    file_id = H5Fcreate(FILE2, H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

    for(int moo=0;moo<SetRankOut;moo++)
      DimsInv[moo]=DimsOut[SetRankOut-moo-1];

    for(int moo=0;moo<FieldRankOut;moo++)
      field_dims_attr[moo]=DimsOut[moo];

    //Create Dataspace 
    dataspace_id=H5Screate_simple(SetRankOut, DimsInv, NULL);
    
    //create set
    //                       duh, name,      datatype,  shape of data, Something I dont get
    dataset_id = H5Dcreate(file_id, SET_ID_OUT, float_type_id, dataspace_id, H5P_DEFAULT);
    
    //
    // The Attribute melee
    //

    //rank
    attr_count = 1;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    component_rank_attr = ComponentRankOut;
    attr_id = H5Acreate(dataset_id, "Component_Rank",  HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    h5_status = H5Awrite(attr_id,  HDF5_I4, &component_rank_attr);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);


    //size
    attr_count = 1;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "Component_Size",  HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    component_size_attr = 2097152;
    h5_status = H5Awrite(attr_id,  HDF5_I4, &component_size_attr);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);

    attr_count = 1;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "Rank", HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    field_rank_attr = 3;//outdims; ?
    h5_status = H5Awrite(attr_id,  HDF5_I4, &field_rank_attr);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);

    //this shit is broke.
    attr_count = FieldRankOut;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "Dimensions", HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    h5_status = H5Awrite(attr_id,  HDF5_I4, field_dims_attr);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);
    
    /*    attr_count = 3;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "TopGridStart", HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    h5_status = H5Awrite(attr_id,  HDF5_I4, Starts);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);
    
    attr_count = 3;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "TopGridEnd", HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    h5_status = H5Awrite(attr_id,  HDF5_I4, Ends);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);
    
    attr_count = 3;
    attr_dsp_id = H5Screate_simple(1, &attr_count, NULL);
    attr_id = H5Acreate(dataset_id, "TopGridDims", HDF5_FILE_I4, attr_dsp_id, H5P_DEFAULT);
    h5_status = H5Awrite(attr_id,  HDF5_I4, Tops);
    h5_status = H5Aclose(attr_id);
    h5_status = H5Sclose(attr_dsp_id);
*/
    //Write the Data Set
    //                (set, memory type, mem. space, file space, transfer shit, actual data)
    fprintf(stderr,"Writing set\n");
    status = H5Dwrite(dataset_id, float_type_id, H5S_ALL, H5S_ALL, H5P_DEFAULT, 
		      DataOut);
    
    
    status = H5Sclose(dataspace_id);
    status = H5Dclose(dataset_id);
    status = H5Fclose(file_id);
  }//Write    

  if( DataIn != NULL )
    delete [] DataIn;

  if( DataOut != NULL )
    delete [] DataOut;
  
}
