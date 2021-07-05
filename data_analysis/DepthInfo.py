from ColumnReferences import ColumnReferences

class DepthInfo:
    """Commom Depth class for all turtle's data """
    
    def __init__(self, npEntry):
        self.depth_id = npEntry[ColumnReferences.DEPTH_DEPTH_ID]
        self.nogps_id = npEntry[ColumnReferences.DEPTH_NOGPS_ID]
        self.acquisitionTime = npEntry[ColumnReferences.DEPTH_ACQUISITION_TIME]
        self.acquisitionStartTime = npEntry[ColumnReferences.DEPTH_ACQUISITION_START_TIME]
        self.underwaterPercentage = npEntry[ColumnReferences.DEPTH_UNDERWATER_PERCENTAGE]
        self.diveCount = npEntry[ColumnReferences.DEPTH_DIVE_COUNT]
        self.averageDiveDuration = npEntry[ColumnReferences.DEPTH_AVERAGE_DIVE_DURATION]
        self.maximumDiveDuration = npEntry[ColumnReferences.DEPTH_MAXIMUM_DIVE_DURATION]
        self.maximumDiveDepth = npEntry[ColumnReferences.DEPTH_MAXIMUM_DIVE_DEPTH]
        self.percentageLayer1 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER1]
        self.percentageLayer2 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER2]
        self.percentageLayer3 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER3]
        self.percentageLayer4 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER4]
        self.percentageLayer5 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER5]
        self.percentageLayer6 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER6]
        self.percentageLayer7 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER7]
        self.percentageLayer8 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER8]
        self.percentageLayer9 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER9]
        self.percentageLayer10 = npEntry[ColumnReferences.DEPTH_PERCENTAGE_LAYER10]
        self.diveCountLayer1 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER1]
        self.diveCountLayer2 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER2]
        self.diveCountLayer3 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER3]
        self.diveCountLayer4 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER4]
        self.diveCountLayer5 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER5]
        self.diveCountLayer6 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER6]
        self.diveCountLayer7 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER7]
        self.diveCountLayer8 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER8]
        self.diveCountLayer9 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER9]
        self.diveCountLayer10 = npEntry[ColumnReferences.DEPTH_DIVE_COUNT_LAYER10]
        self.halfTime = (convertUnixTimeFromString(self.acquisitionTime) + convertUnixTimeFromString(self.acquisitionStartTime))/2
