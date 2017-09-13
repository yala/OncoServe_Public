# OncoServe

## Big Picture
OncoNet trains model using Pytorch to classify binary pathology categories.
OncoServe should wrap the model in a server that allows it to return outputs in real time.

## Github
https://github.com/clarali210/OncoServe

Make sure Master branch is clean by creating separate branches and cross-checking merge requests. Test scripts should run before each push. This way we can have reliable version control to default back on.

## Structure

### User interface
- Using Flask
- Currently can:
  - Upload image
  - Select pre-trained models from dropdown
  - Return prediction/errors
  - Display uploaded image
- To do:
	- Add some JS/CSS to make it prettier
	- Options to upload entire folder / multiple files
  - Drag and drop upload
  - Add different options to aggregate results
  - Loading gif when model is loading

### Model
- Eventually will load from OncoNet
- Using pre-trained torchvision models for now
- Currently can:
  - Load pre-trained models from torchvision
- To do:
  - Convert images from dicoms to png format (examples on cbis-ddsm)
  - Connect to OncoNet

### Unit Tests
- A script that can test the client by inputting images from ImgNet and returning an output
- Tests for individual components of the model
- Using Python requests
- Currently can:
  - Send one image post request and output results in terminal
- To do
  - Write a for loop for multiple images
  - Test automatically before git push

### Error Logging
- When an error occurs, log the error in a file
- Use Pylogger
- Currently can:
  - Display errors in browser
- To do:
  - Use logger to save in log file

### Environment and Portability
- Wrap all the necessary libraries in a light VM for modular setup
- Use Docker or Singularity
	- https://docs.docker.com/get-started/
  - http://singularity.lbl.gov/
 
 
