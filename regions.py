class Regions(object):

    def __init__(self, a, b, c, d, x, y):
        self.minY = a
        self.maxX = b
        self.maxY = c
        self.minX = d
        self.totalColumns = x
        self.totalRows = y
        self.totalXintercepts = x + 1
        self.totalYintercepts = y + 1
        self.totalIntercepts = x + y
        self.totalRegions = x * y

    def resolution(self):
        return self.width(), self.height()

    def width(self):
        width = self.maxX - self.minX
        return width

    def height(self):
        height = self.maxY - self.minY
        return height

    def xIntercepts(self):
        totalIntercepts =self.totalXintercepts
        constant = self.width() / self.totalRows
        intercepts =  [[] for i in range(totalIntercepts)]
        reference = self.minX
        for i in range(totalIntercepts):
            intercepts[i] = reference
            reference = reference + constant
        return intercepts

    def yIntercepts(self):
        totalIntercepts = self.totalYintercepts
        constant = self.height() / self.totalRows
        intercepts =  [ [] for i in range(totalIntercepts)]
        reference = self.minX
        for i in range(totalIntercepts):
            intercepts[i] = reference
            reference = reference + constant
        return intercepts

    def regions(self):
        totalLists = self.totalRegions
        #create a list
        regions = [ [] for i in range(totalLists)]
        indexX = 0
        indexY = 0
        rowCount = 0
        columnCount = 0
        for i in range(totalLists):
            a = self.xIntercepts()[indexX]      
            b = self.xIntercepts()[indexX + 1]  
            c = self.yIntercepts()[indexY + 1]  
            d = self.yIntercepts()[indexY]      
            regions[i]=(a,b,c,d)

            rowCount = rowCount + 1
            columnCount = columnCount + 1

            if rowCount < self.totalColumns:
                indexX = indexX + 1

            elif rowCount == self.totalColumns:
                indexX = 0
                rowCount = 0

            if columnCount == self.totalColumns:
                indexY = indexY + 1
                columnCount = 0

        return regions

    def checkRegion(self, x, y):
        index = 0
        for a in self.regions():
            xMin = a[0]
            xMax = a[1]
            yMin = a[3]
            yMax = a[2]
            index += 1
            if((x >= xMin) and (x <= xMax)) and ((y >= yMin) and (y <= yMax)):
                    return index

    def center(self):
        index = 0
        centers =  [ [] for i in range(self.totalRegions)]
        for i in range(self.totalYintercepts-1):
            for ii in range(self.totalXintercepts-1):
                x1 = self.xIntercepts()[ii]
                x2 = self.xIntercepts()[ii + 1]
                y1 = self.yIntercepts()[i]
                y2 = self.yIntercepts()[i+1]

                x = (x2 - x1) / 2
                y = (y2 - y1) / 2
                centers[index] = x1 + x, y1 + y
                index = index + 1

        return centers

if __name__ == "__main__":
    region = Regions(0, 480, 480,0, 3, 3)
    print (region.totalXintercepts)
