import pandas as pd

class FaceGlyph:
    
    def __init__(self):
        self.traits = ["facesize", "eyebrows", "eye_size", "eye_slant", "nose", "mouth", "emotion"]
        self.properties = []
        self.cols = []
        self.maxs = {}
        for trait in self.traits:
            self.maxs[trait] = None
        self.mins = {}
        for trait in self.traits:
            self.mins[trait] = None


    def add_data(self, data, facesize = None, eyebrows = None, eye_size = None, 
                 eye_slant = None, nose = None, mouth = None, emotion = None, emotion_keep_sign = False):
        """ 
        add data to scale face glyphs.

        parameters:
        - data: pandas data frame containing data
        - facesize: string, colname in the pandas data frame that is being matched to the face size
        - eyebrows: string, colname in the pandas data frame that is being matched to the eyebrow size
        - eye_size: string, colname in the pandas data frame that is being matched to the eye size
        - eye_slant: string, colname in the pandas data frame that is being matched to the eye slant
        - nose: string, colname in the pandas data frame that is being matched to the nose size
        - mouth: string, colname in the pandas data frame that is being matched to the mouth size
        - emotion: string, colname in the pandas data frame that is being matched to the emotion

        note that the data does NOT need to be scaled
        """
        self.data = data
        self.emotion_keep_sign = emotion_keep_sign
        for i, colname in enumerate([facesize, eyebrows, eye_size, eye_slant, nose, mouth, emotion]):
            if colname is not None:
                self.maxs[self.traits[i]] = data.max(axis=0)[colname]
                self.mins[self.traits[i]] = data.min(axis=0)[colname]
                self.properties.append(self.traits[i])
                self.cols.append(colname)

    def latex(self, index):
        """ 
        returns latex expression to copy and paste that creates the face glyph to the data point indicated by index.
        If one facial trait is not being mapped to, it defaults to 0. 

        parameters:
        - index: int

        returns:
        - out: string, Latex expression
        """
        # rescale each property from [min, max] onto [0,1]
        instance = self.data.iloc[index].to_dict()
        values = {}
        for i, prop in enumerate(self.properties):
            if prop == "eye_slant":
                scale = lambda x: ( (2*  (x - self.mins[prop])/(self.maxs[prop]-self.mins[prop])) - 1)
            elif prop == "emotion" and self.emotion_keep_sign:
                continue
            else:
                scale = lambda x: (x - self.mins[prop])/(self.maxs[prop]-self.mins[prop])
            values[prop] = round(scale(instance[self.cols[i]]),3)

        out = "\\faceglyph"
        for trait in self.traits:
            if trait in self.properties:
                if trait == "emotion":
                    continue
                out = out + "{{{}}}".format(values[trait])
            else:
                if trait == "emotion":
                    continue
                out = out + "{{{}}}".format(0)
        
        if "emotion" in self.properties:
            if self.emotion_keep_sign:
                if instance[self.cols[-1]] >= 0:
                    values["emotion"] = round(instance[self.cols[-1]]/self.maxs["emotion"],3)
                    out = out + "{{\\happiness{{{}}}}}".format(values["emotion"])
                else:
                    values["emotion"] = round(instance[self.cols[-1]]/self.mins["emotion"],3)
                    out = out + "{{\\sadness{{{}}}}}".format(values["emotion"])
            else:
                if values["emotion"] >= 0.5:
                    out = out + "{{\\happiness{{{}}}}}".format(round(2*values[trait]-1,3))
                else:
                    out = out + "{{\\sadness{{{}}}}}".format(round(1-2*values[trait],3))
        else:
            out = out + "{\\neutral}"
        print(out)