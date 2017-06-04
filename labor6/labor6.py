import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# labor6
#

class labor6(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "labor6" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mateusz Muszer (PolSl)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    ...
""" # replace with organization, grant and thanks.

#
# labor6Widget
#

class labor6Widget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLModelNode"] # ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input model." )
    parametersFormLayout.addRow("Input model: ", self.inputSelector)

    #
    # transparency value
    #
    self.modelTransparencySliderWidget = ctk.ctkSliderWidget()
    self.modelTransparencySliderWidget.singleStep = 1
    self.modelTransparencySliderWidget.minimum = 0
    self.modelTransparencySliderWidget.maximum = 100
    self.modelTransparencySliderWidget.value = 0
    self.modelTransparencySliderWidget.setToolTip("Set transparency.")
    parametersFormLayout.addRow("Model transparency: ", self.modelTransparencySliderWidget)

    #
    # Apply Button
    #
    self.showHideButton = qt.QPushButton("Show/hide")
    self.showHideButton.toolTip = "Show/hide selected model."
    self.showHideButton.enabled = False
    parametersFormLayout.addRow(self.showHideButton)

    # connections
    self.showHideButton.connect('clicked(bool)', self.onShowHideButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.modelTransparencySliderWidget.connect('valueChanged(double)', self.onSliderChange)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    logic = labor6Logic()
    self.showHideButton.enabled = self.inputSelector.currentNode()
    if logic.hasModelData(self.inputSelector.currentNode()):
      modelTransparency = self.modelTransparencySliderWidget.value
      logic.setTransparency(self.inputSelector.currentNode().GetDisplayNode(), modelTransparency)

  def onShowHideButton(self):
    logic = labor6Logic()
    logic.setVisibility(self.inputSelector.currentNode().GetDisplayNode())
	
  def onSliderChange(self):
    logic = labor6Logic()
    if logic.hasModelData(self.inputSelector.currentNode()):
      modelTransparency = self.modelTransparencySliderWidget.value
      logic.setTransparency(self.inputSelector.currentNode().GetDisplayNode(), modelTransparency)

#
# labor6Logic
#

class labor6Logic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
  def hasModelData(self,modelNode):
    if not modelNode:
      logging.debug('hasModelData failed: no model node')
      return False
    
    return True
  
  
  def setTransparency(self,inputModel, modelTransparency):
      inputModel.SetOpacity((100-modelTransparency)/100)
	  
  def setVisibility(self, inputModel):
      inputModel.VisibilityOff() if inputModel.GetVisibility() else inputModel.VisibilityOn()


class labor6Test(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_labor61()

  def test_labor61(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = labor6Logic()
    self.assertIsNotNone( logic.hasModelData(volumeNode) )
    self.delayDisplay('Test passed!')
