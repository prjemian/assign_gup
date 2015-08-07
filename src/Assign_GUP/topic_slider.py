
'''
add label, slider, value to a QGridLayout

Coordinate the action of a slider with the topic value::

  label   slider                    value
  bio     -|---|---|---|[-]|---|-   0.7
  phys    -|--[|]--|---|---|---|-   0.2

======  =========  ====================================================
widget  type       description
======  =========  ====================================================
label   QLabel     mnemonic name (no white space)
slider  QSlider    graphical adjustment of value
value   QLineEdit  string with floating point value: 0 <= value <= 1.0
======  =========  ====================================================

These three widgets will be added to the *parent* widget,
assumed to be on the same row of a QGridLayout.

A *topic* (known here as *label*) is some scientific area 
of interest to the PRP.
Such as, for the SAXS review panel, some of the proposals
are for XPCS (X-ray Photon Correlation Spectroscopy).

Each proposal will have a strength value assigned for
each topic, indicating how important that topic is to the
proposed experiment.

Each reviewer will have a strength value assigned for
each topic, indicating the strength of that reviewer 
in the particular topic.
'''


from PyQt4 import QtGui, QtCore

class AGUP_TopicSlider(QtCore.QObject):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent, row, label, value):
        self.slider_factor = 100    # slider = slider_factor * value_widget

        self.slider = QtGui.QSlider(
                                value=int(self.slider_factor*value),
                                maximum=self.slider_factor,
                                pageStep=10,
                                tracking=False,
                                orientation=QtCore.Qt.Horizontal,
                                tickPosition=QtGui.QSlider.TicksBothSides,
                                tickInterval=20
                               )

        self.value_widget = QtGui.QLineEdit(str(value))
        self.value_widget.setMaximumWidth(self.slider_factor)
        
        self.label = label
        self.parent = parent
        self.value = value

        parent.addWidget(QtGui.QLabel(label), row, 0)
        parent.addWidget(self.slider, row, 1)
        parent.addWidget(self.value_widget, row, 2)
        
        # connect slider changes with value_widget and vice versa
        self.slider.valueChanged.connect(self.onSliderChange)
        self.slider.sliderMoved.connect(self.onSliderChange)
        self.value_widget.textEdited.connect(self.onValueChange)
    
    def onSliderChange(self, value):
        self.setValue(str(value / float(self.slider_factor)))
    
    def onValueChange(self, value):
        try:
            float_value = float(value)
            if 0 <= float_value <= 1.0:
                self.setSliderValue(int(float_value*self.slider_factor))
        except ValueError, exc:
            # TODO: send to the logger
            print self.label, exc

    def getValue(self):
        # if can't convert, get value from slider
        try:
            value = float(self.value_widget.text())
        except ValueError, exc:
            value = self.getSliderValue() / float(self.slider_factor)
        return value
    
    def setValue(self, value):
        '''
        set strength of this topic (0:low, 1.0: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the slider value.
        '''
        self.value_widget.setText(str(value))
    
    def getSliderValue(self):
        value = self.slider.value()
        return value
    
    def setSliderValue(self, value):
        '''
        set value of the slider indicating strength of this topic (0:low, 100: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the text value.
        '''
        self.slider.setValue(value)
