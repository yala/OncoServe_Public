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
  - Loading gif when model is loading
  - Add different options to aggregate results
  - Options to upload multiple files
- To do:
	- Add some JS/CSS to make it prettier
  - Drag and drop upload

### Model
- Eventually will load from OncoNet
- Using pre-trained torchvision models for now
- Currently can:
  - Load pre-trained models from torchvision
- To do:
  - Connect to OncoNet

### Unit Tests
- A script that can test the client by inputting images from ImgNet and returning an output
- Tests for individual components of the model
- Using Python requests
- Currently can:
  - Send multiple image post request with model and aggregation configurations and output results in terminal
- To do
  - Upload a folder instead of individual images
  - Test automatically before git push

### Error Logging
- When an error occurs, log the error in a file
- Use Pylogger
- Currently can:
  - Display errors in browser
  - Use logger to save in log file
- To do:

### Environment and Portability
- Wrap all the necessary libraries in a light VM for modular setup
- Use Docker or Singularity
	- https://docs.docker.com/get-started/
  - http://singularity.lbl.gov/
 
 
