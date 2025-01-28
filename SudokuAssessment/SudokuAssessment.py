# board class
class SudokuBoard:
  # initialisation function creates empty board data list
  def __init__(x):
    x.boardData = []
    emptyCell = ("Input",0)
    for i in range(81):
       x.boardData.append(emptyCell)
  # get function for entire board 
  def getBoard(x):
     return x.boardData
  # get function for cell data
  def getCellData(self, coord):
      return self.boardData[coord]
    # get function for cell type
  # get function for cell type
  def getCellType(self, coord):
      try:
        x = self.boardData[coord][0]
      except:
        x = "Error"
        print("error")
      return x
  # get function for cell value
  def getCellValue(self, coord):
     try:
        x = self.boardData[coord][1]
     except:
        x = 0
        print("error")
     return x
  # set function for cell data
  def setCellData(self, coord, cellType, cellValue):
     cellData = (cellType, cellValue)
     try:
        self.boardData[coord] = cellData
     except:
        print("error")
  # set function for cell Type
  def setCellType(self, coord, cellType):
     cellValue = self.getCellValue(coord)
     self.setCellData(self,coord,cellType,cellValue)
  # set function for cell value
  def setCellValue(self, coord, cellValue):
     cellType = self.getCellType(coord)
     self.setCellData(self,coord,cellType,cellValue)

p1 = SudokuBoard()
print(p1.getCellData(1))
print(p1.getCellType(1))
print(p1.getCellValue(1))
p1.setCellData(3,("clue", 3))
print(p1.getCellData(3))
