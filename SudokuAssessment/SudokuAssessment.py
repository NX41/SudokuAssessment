from http.client import FORBIDDEN
import math
from multiprocessing.sharedctypes import SynchronizedBase
from re import L, S
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time

# board class
class SudokuBoard:
  # initialisation function creates empty board data list
  def __init__(self):
    boardData = []
    self.boardData = boardData
    emptyCell = ("Input",0,[])
    for i in range(82):
        self.boardData.append(emptyCell)  
  # get function for entire board 
  def getBoard(x):
     return x.boardData
  # get function for cell data
  def getCellData(a, coord):
      return a.boardData[coord]
    # get function for cell type
  # get function for cell type
  def getCellType(self, coord):
      try:
        x = self.boardData[coord][0]
      except:
        x = "Error"
        print("error, failed to get cell type")
      return x
  # get function for cell value
  def getCellValue(self, coord):
     try:
        x = self.boardData[coord][1]
        return x
     except:
        print("error no value")
  # get function for cell rules
  def getCellRules(self,coord):
     try:
        x = self.boardData[coord][2]
        return x
     except:
        print("error, failed to get cell rules")
  # set function for cell data
  def setCellData(self, coord, cellType, cellValue, cellRules):
     cellData = (cellType, cellValue, cellRules)
     try:
        self.boardData[coord] = cellData
        # print("Set Cell "+str(coord)+", Set Type to "+cellType+", Set Value to "+str(cellValue)+" with Rules: "+str(cellRules))
     except:
        print("error, could not set cell data")
  # set function for cell Type
  def setCellType(self, coord, cellType):
     cellValue = self.getCellValue(coord)
     cellRules = self.getCellRules(coord)
     self.setCellData(coord,cellType,cellValue,cellRules)
  # set function for cell value
  def setCellValue(self, coord, cellValue):
     cellType = self.getCellType(coord)
     cellRules = self.getCellRules(coord)
     self.setCellData(coord,cellType,cellValue,cellRules)
  # set function for cell rules
  def setCellRules(self, coord, rules):
     cellType = self.getCellType(coord)
     cellValue = self.getCellValue(coord)
     self.setCellData(coord,cellType,cellValue,rules)
  # add rule to cell
  def addCellRule(self, coord, rule):
     currentRules = self.getCellRules(coord)
     newRules = currentRules.copy()
     newRules.append(rule)
     self.setCellRules(coord,newRules)
  # remove rule from cell
  def removeCellRule(self, coord, rule):
     cellRules = self.getCellRules(coord)
     cellRules.remove(rule)
     self.setCellRules(coord, cellRules)
  
     
  # save file
  def saveFile(self, fName):
       f = open(f"{fName}.txt", "w")
       print("test")
       for i in range(1,82):
          f.write(str(self.getCellData(i)))
          f.write(",")
       f.close()
  # load file
  def readFile(self, fName):
     with open(f"{fName}.txt", "w") as f:
        f.readline()
     f.close()


# rules
class boardRules():
   def __init__(self):
      rulesList = {
         
         }
      self.rulesList = rulesList
   # get rule function
   def getRuleList(self):
      return self.rulesList
   # get rule by name function 
   def getRuleByName(self,RuleName):
      RulesReturn = self.rulesList[RuleName]
      return RulesReturn 
   # get rule list names
   def getRuleListNames(self):
      RulesListNames = []
      for x in self.rulesList.keys():
         RulesListNames.append(x)
      return RulesListNames
   # add rule to list
   def addRule(self,RuleName,RuleType,cellList,Sboard):
      inputRule = [RuleType,cellList]
      self.rulesList[RuleName] = inputRule
      
      if RuleType == "killer":
         for i in cellList[1:]:
            Sboard.addCellRule(i,RuleName)
      else:
         for i in cellList:
            Sboard.addCellRule(i,RuleName)
   # remove rule to list
   def removeRule(self,RuleName,Sboard):
      for i in self.rulesList[RuleName][1]:
        Sboard.removeCellRule(i, RuleName)
      self.rulesList.pop(RuleName)
# add default rules
   def addDefaultRules(self, sBoard):
      # add row rules
      for i in range(0,9):
         genList = []
         for x in range(1,10):
            genList.append((i*9)+x)
         self.addRule(f"rowDefault{i+1}","standard",genList,sBoard)
      # add column rules
      for i in range(1,10):
         genList = []
         for x in range(0,9):
            genList.append((x*9)+i)
         self.addRule(f"columnDefault{i}","standard",genList,sBoard)   
      # add sub-grid rules
      i = 0
      for lY in range(0,7,3):
        for lX in range(0,7,3):
            genList = []
            for y in range(0,3):
                for x in range(1,4):
                    genList.append((x+lX)+((y+lY)*9))
            i += 1
            self.addRule(f"subgridDefault{i}","standard",genList,sBoard) 
# board validator
   def testRuleValid(self, RuleName, sBoard):
      if(self.rulesList[RuleName][0]) == "standard":
         return self.standardRuleTest(RuleName, sBoard)
      elif(self.rulesList[RuleName][0]) == "consecutive":
         return self.consecutiveRuleTest(RuleName, sBoard)
      elif(self.rulesList[RuleName][0]) == "arrow":
         return self.arrowRuleTest(RuleName, sBoard)
      elif(self.rulesList[RuleName][0]) == "thermo":
         return self.thermoRuleTest(RuleName, sBoard)
      elif(self.rulesList[RuleName][0]) == "killer":
         return self.killerRuleTest(RuleName, sBoard)
      elif(self.rulesList[RuleName][0]) == "greater":
         return self.greaterRuleTest(RuleName, sBoard) 
   # standard rule test
   def standardRuleTest(self, RuleName, sBoard):
      FoundValues = []
      for i in self.rulesList[RuleName][1]:
         currentValue = sBoard.getCellValue(i)
         if sBoard.getCellValue(i) in FoundValues:
            return "Invalid"
         else:
            if currentValue != 0:
                FoundValues.append(currentValue)
      return "Valid"
   # consecutive rule test
   def consecutiveRuleTest(self, RuleName, sBoard):
      FoundValues = []
      for i in self.rulesList[RuleName][1]:
         currentValue = sBoard.getCellValue(i)
         if sBoard.getCellValue(i) in FoundValues:
            
            print("Found: Invalid")
            return "Invalid"
         else:
            if currentValue != 0:
                FoundValues.append(currentValue)
      print("Valid list entry, testing consecutive")
      FoundValues.sort()
      for i in range(1, len(FoundValues)):
         x = FoundValues[i-1]
         x = int(x) + 1
         y = int(FoundValues[i])
         if x != y:
             return "Invalid"
      return "Valid"
   # arrow rule test
   def arrowRuleTest(self, RuleName, sBoard):
      ReachValue = sBoard.getCellValue(self.rulesList[RuleName][1][0])
      FoundValues = []
      for i in self.rulesList[RuleName][1][1:]:
         FoundValues.append(sBoard.getCellValue(i))
      SumValue = math.fsum(FoundValues)
      if SumValue > ReachValue:
         print(f"{RuleName} Inalid")
         return "Invalid"
      else:
         print(f"{RuleName} Valid")
         return "Valid"
   # thermo rule test
   def thermoRuleTest(self, RuleName, sBoard):
      FoundValues = []
      for i in self.rulesList[RuleName][1]:
         FoundValues.append(sBoard.getCellValue(i))
      for i in range(1, len(FoundValues)):
         x = FoundValues[i-1]
         x = int(x)
         y = int(FoundValues[i])
         if x > y:
             return "Invalid"
      return "Valid"
   # killer rule test
   def killerRuleTest(self, RuleName, sBoard):
      ReachValue = self.rulesList[RuleName][1][0]
      print(ReachValue)
      FoundValues = []
      for i in self.rulesList[RuleName][1][1:]:
         FoundValues.append(sBoard.getCellValue(i))
      print(FoundValues)
      SumValue = math.fsum(FoundValues)
      print(SumValue)
      if SumValue == ReachValue:
         print(f"{RuleName} Valid")
         return "Valid"
      else:
         print(f"{RuleName} Inalid")
         return "Invalid"
   # greater region
   def greaterRuleTest(self, RuleName, sBoard):
      GreaterValue = sBoard.getCellValue(self.rulesList[RuleName][1][0])
      LesserValue = sBoard.getCellValue(self.rulesList[RuleName][1][1])
      if GreaterValue > LesserValue:
         print(f"{RuleName} Valid")
         return "Valid"
      else:
         print(f"{RuleName} Invalid")
         return "Invalid"
   # test cell rules
   def testCellRules(self, coord, sBoard):
      cellRule = sBoard.getCellRules(coord).copy()
      for i in cellRule:
         if self.testRuleValid(i,sBoard) == "Invalid":
            return "Invalid"
      return "Valid"
   # solving algorithm
    # brute force
   def bruteSolvingAlg(self, sBoard, currentCell = 1, ):
       while currentCell != 82:
           if sBoard.getCellType(currentCell) == "Input":
                 valid = self.incrementer(currentCell, sBoard)
                 if valid == "Invalid":
                    sBoard.setCellValue(currentCell, 0)
                    currentCell -= 1
                    while sBoard.getCellType(currentCell) != "Input":
                        currentCell -= 1
                 else:
                    currentCell += 1
           else:
               currentCell += 1
       else:
          return "Completion"
   # incrementer
   def incrementer(self, currentCell, sBoard):
       valid = "Invalid"
       currentValue = sBoard.getCellValue(currentCell)
       while valid == "Invalid" and currentValue < 9:
          currentValue = sBoard.getCellValue(currentCell)
          currentValue += 1
          sBoard.setCellValue(currentCell, currentValue)
          valid = self.testCellRules(currentCell, sBoard)
       else:
          return valid
   # constraint solving
   def constraintSolvingAlg(self, sBoard, currentCell = 1):
       # add constraints
       forbiddenList = ['test',[],[],[],[],[],[],[],[],[]]
       for i in range(1,82):
          if sBoard.getCellType(i) == "Clue":
             clueValue = sBoard.getCellValue(i)
             cRules = sBoard.getCellRules(i)
             for n in cRules:
                currentRule = self.getRuleByName(n)
                forbiddenList[clueValue].extend(currentRule[1])

       while currentCell != 82:
           if sBoard.getCellType(currentCell) == "Input":
                 valid = self.conIncrementer(forbiddenList, currentCell, sBoard)
                 if valid == "Invalid":
                    sBoard.setCellValue(currentCell, 0)
                    currentCell -= 1
                    while sBoard.getCellType(currentCell) != "Input":
                        currentCell -= 1
                 else:
                    currentCell += 1
           else:
               currentCell += 1
       else:
          return "Completion"
   # constraint incrementor
   def conIncrementer(self, forbiddenList, currentCell, sBoard):
       valid = "Invalid"
       currentValue = sBoard.getCellValue(currentCell)
       while valid == "Invalid" and currentValue < 9:
          currentValue = sBoard.getCellValue(currentCell)
          currentValue += 1
          while currentCell in forbiddenList[currentValue] and currentValue < 9:
             currentValue += 1
          sBoard.setCellValue(currentCell, currentValue)
          valid = self.testCellRules(currentCell, sBoard)
       else:
          return valid
   # constraint solving 2
   def constraintSolvingAlg2(self, sBoard, currentCell = 1):
       # add constraints
       forbiddenList = ['test',[],[],[],[],[],[],[],[],[]]
       for i in range(1,82):
          if sBoard.getCellType(i) == "Clue":
             clueValue = sBoard.getCellValue(i)
             cRules = sBoard.getCellRules(i)
             for n in cRules:
                currentRule = self.getRuleByName(n)
                forbiddenList[clueValue].extend(currentRule[1])

       while currentCell != 82:
           if sBoard.getCellType(currentCell) == "Input":
                 valid = self.conIncrementer(forbiddenList, currentCell, sBoard)
                 if valid == "Invalid":
                    sBoard.setCellValue(currentCell, 0)
                    currentCell -= 1
                    while sBoard.getCellType(currentCell) != "Input":
                        currentCell -= 1
                    # remove from forbidden list
                    clueValue = sBoard.getCellValue(currentCell)
                    cRules = sBoard.getCellRules(currentCell)
                    for n in cRules:
                        currentRule = self.getRuleByName(n)
                        for r in currentRule[1]:
                            forbiddenList[clueValue].remove(r)
                 else:
                    # add to forbidden list
                    clueValue = sBoard.getCellValue(currentCell)
                    cRules = sBoard.getCellRules(currentCell)
                    for n in cRules:
                        currentRule = self.getRuleByName(n)
                        forbiddenList[clueValue].extend(currentRule[1])
                    currentCell += 1
           else:
               currentCell += 1
       else:
          return "Completion"
   # exact solving 1
   def exactSolvingAlg(self, sBoard):
       # add constraints
       forbiddenList = ['test',[],[],[],[],[],[],[],[],[]]
       for i in range(1,82):
          if sBoard.getCellType(i) == "Clue":
             clueValue = sBoard.getCellValue(i)
             cRules = sBoard.getCellRules(i)
             for n in cRules:
                currentRule = self.getRuleByName(n)
                forbiddenList[clueValue].extend(currentRule[1])
             for aln in range(1,10):
                forbiddenList[aln].append(i)
       # exact cover
       completed = False
       loop = 0
       while completed == False:
          added = False
          loop +=1
          for i in self.rulesList:
              for targetValue in range(1,10):
                  newlist = self.rulesList[i][1].copy()
                  for x in self.rulesList[i][1]:
                      if x in forbiddenList[targetValue]:
                          newlist.remove(x)
                  if len(newlist) == 1 and sBoard.getCellValue(newlist[0]) == 0:
                     sBoard.setCellValue(newlist[0], targetValue)
                     added = True
                     cRules = sBoard.getCellRules(newlist[0])
                     for n in cRules:
                        currentRule = self.getRuleByName(n)
                        for lnd in currentRule[1]:
                            if lnd not in forbiddenList[targetValue]:
                               forbiddenList[targetValue].append(lnd)
                     for aln in range(1,10):
                        if newlist[0] not in forbiddenList[aln]:
                            forbiddenList[aln].append(newlist[0])
          if added == True:
              completed = False
          else:
             if loop == 1:
                self.constraintSolvingAlg2(sBoard) 
                break
             else:
                completed = True
       return "completion"
   # exact solving 2
   def exactSolvingAlg2(self, sBoard):
       # add constraints
       forbiddenList = ['test',[],[],[],[],[],[],[],[],[]]

       for i in self.rulesList:
          if self.rulesList[i][0] == "standard":
              for x in self.rulesList[i][1]:
                 scanCell = sBoard.getCellValue(x)
                 if scanCell != 0:
                    for n in self.rulesList[i][1]:
                       if n not in forbiddenList[scanCell]:
                          forbiddenList[scanCell].append(n)
                    for t in range(1,10):
                       if x not in forbiddenList[t]:
                           forbiddenList[t].append(x)
          elif self.rulesList[i][0] == "greater":
             for t in range(1,10):
                if self.rulesList[i][1][1] not in forbiddenList[t]:
                   for r in range(1,t):
                      if self.rulesList[i][1][0] not in forbiddenList[r]:
                        forbiddenList[r].append(self.rulesList[i][1][0])
          # if rule testing is a thermometer rule
          elif self.rulesList[i][0] == "thermo":
             for Pos in range(1, len(self.rulesList[i][1])):                          # loop for all values covered by rule from fisrt to last
                for targetV in range(1,10):                                               # loop for values 1 to 9
                    if self.rulesList[i][1][Pos] not in forbiddenList[targetV]:           # 
                       if self.rulesList[i][1][Pos-1] in forbiddenList[targetV]:
                          forbiddenList[targetV].append(self.rulesList[i][1][Pos])
          
       print(forbiddenList)
       # exact cover
       completed = False
       loop = 0
       while completed == False:
          added = False
          loop +=1
          for i in self.rulesList:
              
                  for targetValue in range(1,10):
                      newlist = self.rulesList[i][1].copy()
                      for x in self.rulesList[i][1]:
                          if x in forbiddenList[targetValue]:
                              newlist.remove(x)
                      if len(newlist) == 1 and sBoard.getCellValue(newlist[0]) == 0:
                         sBoard.setCellValue(newlist[0], targetValue)
                         added = True
                         if self.rulesList[i][0] == "standard":
                            cRules = sBoard.getCellRules(newlist[0])
                            for n in cRules:
                                currentRule = self.getRuleByName(n)
                                for lnd in currentRule[1]:
                                    if lnd not in forbiddenList[targetValue]:
                                       forbiddenList[targetValue].append(lnd)
                         elif  self.rulesList[i][0] == "thermo":
                            for posV in self.rulesList[i][1]:
                               if posV not in forbiddenList[targetValue]:
                                   forbiddenList[targetValue].append(posV)
                         for aln in range(1,10):
                             if newlist[0] not in forbiddenList[aln]:
                                forbiddenList[aln].append(newlist[0])
          if added == True:
              completed = False
          else:
             if loop == 1:
                self.constraintSolvingAlg2(sBoard) 
                break
             else:
                completed = True
       return "completion"
   
   # exact solving 3
   def exactSolvingAlg3(self, sBoard):
       # add constraints
       forbiddenList = []

       for i in range(0,82):
          forbiddenList.append([])
       
       for i in self.rulesList:
          if self.rulesList[i][0] == "standard":
              print(i)
              for x in self.rulesList[i][1]:
                 scanCell = sBoard.getCellValue(x)
                 if scanCell != 0:
                    for n in self.rulesList[i][1]:
                       if scanCell not in forbiddenList[n]:
                          forbiddenList[n].append(scanCell)
          print(forbiddenList)
                          
       print(forbiddenList)
       # exact cover
       completed = False
       loop = 0
       while completed == False:
          added = False
          loop +=1
          for i in self.rulesList:
              
                  for targetValue in range(1,10):
                      newlist = self.rulesList[i][1].copy()
                      for x in self.rulesList[i][1]:
                          if x in forbiddenList[targetValue]:
                              newlist.remove(x)
                      if len(newlist) == 1 and sBoard.getCellValue(newlist[0]) == 0:
                         sBoard.setCellValue(newlist[0], targetValue)
                         added = True
                         if self.rulesList[i][0] == "standard":
                            cRules = sBoard.getCellRules(newlist[0])
                            for n in cRules:
                                currentRule = self.getRuleByName(n)
                                for lnd in currentRule[1]:
                                    if lnd not in forbiddenList[targetValue]:
                                       forbiddenList[targetValue].append(lnd)
                         elif  self.rulesList[i][0] == "thermo":
                            for posV in self.rulesList[i][1]:
                               if posV not in forbiddenList[targetValue]:
                                   forbiddenList[targetValue].append(posV)
                         for aln in range(1,10):
                             if newlist[0] not in forbiddenList[aln]:
                                forbiddenList[aln].append(newlist[0])
          if added == True:
              completed = False
          else:
             if loop == 1:
                self.constraintSolvingAlg2(sBoard) 
                break
             else:
                completed = True
       return "completion"
   # save file 
   def saveFile(self, fName):
       f = open(f"{fName}.txt", "w")
       print("test")
       f.write(str(self.rulesList))
       f.write(",")
       f.close() 
# display
class displayApp(tk.Tk):
    def __init__(self, sBoard, sRules):
        super().__init__()
        self.geometry('1000x600')
        self.title('Sudoku')

        self.sBoard = sBoard
        self.sRules = sRules
        
        self.wholeUpdate = False
        # main frame setup
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.rowconfigure(1, weight=1)
       

        # board frame
        boardframe = ttk.Labelframe(self, text='Board', padding='5', width=1000)
        boardframe.grid(column=0, row=0, sticky="news")
         
        # rules list
        rulesListVar = sRules.getRuleListNames()
        varRuleListBox = tk.Variable(value=rulesListVar)
        self.rulesList = tk.Listbox(boardframe, listvariable=varRuleListBox)
        self.rulesList.grid(column=0, row=0, sticky="ns")
        # board canvas
        self.canvas = tk.Canvas(boardframe, width=500, height=500, bg='white')
        self.canvas.grid(column=1, row=0,sticky="news")
        # canvas draw
        for cellCoord in range(1,82):
            cellX = self.convertCoordx(cellCoord)
            cellY = self.convertCoordy(cellCoord)
            self.canvas.create_rectangle(
                ((cellX*50)-25, ((cellY)*50)-25),
                ((cellX*50)+25, ((cellY)*50)+25),
                )
            if sBoard.getCellValue(cellCoord) != 0:
                textdisplacy =sBoard.getCellValue(cellCoord)
            else:
                textdisplacy = ""
            self.canvas.create_text(
                (cellX*50, cellY*50),
                text=textdisplacy,
                fill="black",
                font=self.ifCluBold(sBoard, cellCoord)
                )
        for cellX in range(25,450,150):
            for cellY in range(25,450,150):
                self.canvas.create_rectangle(
                    ((cellX), ((cellY))),
                    (((cellX+150)), ((cellY+150))),
                    width=3
                    )
        # text input box
        self.consoleFrame = tk.Frame(boardframe)  
        self.consoleFrame.grid(column=2, row=0, sticky="nsew")
        ## Console command log
        self.consoleInputList = []
        varconsoleInputList = tk.Variable(value=self.consoleInputList)
        self.inputList = tk.Listbox(self.consoleFrame, height=30, width=50, listvariable=varconsoleInputList)
        self.inputList.grid(column=0, row=0, sticky="we")  
        ## console command input
        self.inputText = tk.StringVar()
        self.inputConsole = tk.Entry(self.consoleFrame, textvariable=self.inputText)
        self.inputConsole.grid(column=0, row=1, sticky="we")   
        self.inputConsole.bind('<Return>', self.commandFunc)
    # command function
    def commandFunc(self, inputS):
       print(self.inputText.get())
       if self.inputText.get() != "":
          self.inputList.insert('end',self.inputText.get())
          commandStr = self.inputText.get()
          CommandL = commandStr.split()
          self.command(CommandL)
          self.inputConsole.delete(0,81)
    # command function real
    def command(self, CommandL):
       try:
          # insert number command
          if CommandL[0] == "insert":
            if int(CommandL[1]) > 0 and int(CommandL[1]) < 10:
                self.inputList.insert('end',f"Inserting {CommandL[1]} into cell ({CommandL[2]} {CommandL[3]})")
                self.sBoard.setCellValue(self.convertCoord(CommandL[2],CommandL[3]),int(CommandL[1]))
                valid = self.sRules.testCellRules(self.convertCoord(CommandL[2],CommandL[3]), self.sBoard)
                if valid == "Invalid":
                    self.inputList.insert('end',"Invalid entry")
                if self.wholeUpdate == True:
                    self.updateWholeCanvas(self.sBoard)
                else:
                    self.updateCanvas(self.convertCoord(CommandL[2],CommandL[3]), valid)
            else:
                self.inputList.insert('end',"Invalid entry")
          # change type command
          elif CommandL[0] == "type":
            if CommandL[1] == "Clue" or CommandL[1] == "Input":
                self.inputList.insert('end',f"Changing cell ({CommandL[2]} {CommandL[3]}) to type {CommandL[1]}")
                self.sBoard.setCellType(self.convertCoord(CommandL[2],CommandL[3]),CommandL[1])
                self.updateCanvas(self.convertCoord(CommandL[2],CommandL[3]), "Valid")
            else:
               self.inputList.insert('end',"invalid type, use either 'Clue' or 'Input'")
          # update whole canvas
          elif CommandL[0] == "update":
             self.updateWholeCanvas(self.sBoard)
          # change update whole
          elif CommandL[0] == "changeupdate":
             if self.wholeUpdate == True:
                self.wholeUpdate = False
                self.inputList.insert('end',"Changed canvas update to singular cell update")
             elif self.wholeUpdate == False:
                self.wholeUpdate = True
                self.inputList.insert('end',"Changed canvas update to whole board update")
          # add rule to board
          elif CommandL[0] == "addrule":
             cellList = [int(x) for x in CommandL[3:]]
             self.inputList.insert('end',f"Adding rule {CommandL[1]} for cells ({cellList})")
             self.sRules.addRule(CommandL[1],CommandL[2],cellList,self.sBoard)
             self.rulesList.insert('end',CommandL[1])
          # remove rule from board
          elif CommandL[0] == "removerule":
             self.inputList.insert('end',f"Removing rule {CommandL[1]}")
             self.sRules.removeRule(CommandL[1],self.sBoard)
             idx = self.rulesList.get(0,'end').index(CommandL[1])
             self.rulesList.delete(idx)
          # run solving algorithm
          elif CommandL[0] == "solve":
             x = time.perf_counter()
             if CommandL[1] == "brute":
                 completion = self.sRules.bruteSolvingAlg(self.sBoard)
             elif CommandL[1] == "con1":
                 completion = self.sRules.constraintSolvingAlg(self.sBoard)
             elif CommandL[1] == "con2":
                 completion = self.sRules.constraintSolvingAlg2(self.sBoard)
             elif CommandL[1] == "exact":
                 completion = self.sRules.exactSolvingAlg(self.sBoard)
             elif CommandL[1] == "exact2":
                 completion = self.sRules.exactSolvingAlg2(self.sBoard)
             elif CommandL[1] == "exact3":
                 completion = self.sRules.exactSolvingAlg3(self.sBoard)
             self.updateWholeCanvas(self.sBoard)
             timeElaspsed = time.perf_counter() - x
             self.inputList.insert('end',f"Algorithm has reached {completion} in {round(timeElaspsed,4)} Seconds")
          # clear board
          elif CommandL[0] == "clear":
             self.clearBoard()
          # clear board full
          elif CommandL[0] == "clearall":
             self.clearBoard(True)
          # save board
          elif CommandL[0] == "save":
             self.sBoard.saveFile(CommandL[1])
          # list all commands#
          elif CommandL[0] == "help":
             if CommandL[1] == "insert":
                self.inputList.insert('end',"command to add values to the board, use insert followed by value followed by x then y.")
             else:
                self.inputList.insert('end',"use commands insert, type, update, updatechange")
                self.inputList.insert('end',"or help then the command for more info")
       except:
            self.inputList.insert('end',"unrecognised command") 
       
    def ifCluBold(self, sBoard, coord):
       if sBoard.getCellType(coord) == "Clue":
          return ('calibre',24,'bold')
       elif  sBoard.getCellType(coord) == "Input":
          return ('calibre',24,'normal')
    # convert coordernates
    def convertCoord(self, cX, cY):
       coord = int(cX)+((int(cY)-1)*9)
       return coord
    def convertCoordx(self, coord):
       x = math.fmod(coord, 9)
       if x == 0:
          x = 9
       return math.ceil(x)
    def convertCoordy(self, coord):
       y = math.ceil(coord/9)
       return y
    # canvas reload
    def updateCanvas(self, coord, valid):
        cellX = self.convertCoordx(coord)
        cellY = self.convertCoordy(coord)
        if valid == "Invalid":
           backfill = "red"
        else:
           backfill = "white"
        self.canvas.create_rectangle(
                    ((cellX*50)-25, ((cellY)*50)-25),
                    ((cellX*50)+25, ((cellY)*50)+25),
                    fill=backfill
                    )
        if self.sBoard.getCellValue(coord) != 0:
            textdisplacy =self.sBoard.getCellValue(coord)
        else:
            textdisplacy = ""
        self.canvas.create_text(
            (cellX*50, cellY*50),
            text=textdisplacy,
            fill="black",
            font=self.ifCluBold(self.sBoard, coord)
            )
        for cellX in range(25,450,150):
            for cellY in range(25,450,150):
                self.canvas.create_rectangle(
                    ((cellX), ((cellY))),
                    (((cellX+150)), ((cellY+150))),
                    width=3
                    )
    # update whole canvas
    def updateWholeCanvas(self, sBoard):
       for i in range(1,82):
          self.updateCanvas(i, self.sRules.testCellRules(i, sBoard))
       print("updated whole canvas")
    
    # clear board function
    def clearBoard(self, full = False):
       for i in range(1,82):
          if self.sBoard.getCellType(i) == "Clue" and full == False:
             pass
          else:
             self.sBoard.setCellValue(i, 0)
          self.updateCanvas(i, self.sBoard)
          
# start up
if __name__ == "__main__":    
    
    p1 = SudokuBoard()
    p2 = boardRules()
    p2.addDefaultRules(p1)
    p1.setCellValue(1,5)
    p1.setCellType(1,"Clue")
    p1.setCellValue(2,3)
    p1.setCellType(2,"Clue")
    p1.setCellValue(5,7)
    p1.setCellType(5,"Clue")
    p1.setCellValue(10,6)
    p1.setCellType(10,"Clue")
    p1.setCellValue(13,1)
    p1.setCellType(13,"Clue")
    p1.setCellValue(14,9)
    p1.setCellType(14,"Clue")
    p1.setCellValue(15,5)
    p1.setCellType(15,"Clue")
    p1.setCellValue(20,9)
    p1.setCellType(20,"Clue")
    p1.setCellValue(21,8)
    p1.setCellType(21,"Clue")
    p1.setCellValue(26,6)
    p1.setCellType(26,"Clue")
    p1.setCellValue(28,8)
    p1.setCellType(28,"Clue")
    p1.setCellValue(32,6)
    p1.setCellType(32,"Clue")
    p1.setCellValue(36,3)
    p1.setCellType(36,"Clue")
    p1.setCellValue(37,4)
    p1.setCellType(37,"Clue")
    p1.setCellValue(40,8)
    p1.setCellType(40,"Clue")
    p1.setCellValue(42,3)
    p1.setCellType(42,"Clue")
    p1.setCellValue(45,1)
    p1.setCellType(45,"Clue")
    p1.setCellValue(46,7)
    p1.setCellType(46,"Clue")
    p1.setCellValue(50,2)
    p1.setCellType(50,"Clue")
    p1.setCellValue(54,6)
    p1.setCellType(54,"Clue")
    p1.setCellValue(56,6)
    p1.setCellType(56,"Clue")
    p1.setCellValue(61,2)
    p1.setCellType(61,"Clue")
    p1.setCellValue(62,8)
    p1.setCellType(62,"Clue")
    p1.setCellValue(67,4)
    p1.setCellType(67,"Clue")
    p1.setCellValue(68,1)
    p1.setCellType(68,"Clue")
    p1.setCellValue(69,9)
    p1.setCellType(69,"Clue")
    p1.setCellValue(72,5)
    p1.setCellType(72,"Clue")
    p1.setCellValue(77,8)
    p1.setCellType(77,"Clue")
    p1.setCellValue(80,7)
    p1.setCellType(80,"Clue")
    p1.setCellValue(81,9)
    p1.setCellType(81,"Clue")
    ## other test board
    # p1.setCellValue(1,8)
    # p1.setCellType(1,"Clue")
    # p1.setCellValue(3,7)
    # p1.setCellType(3,"Clue")
    # p1.setCellValue(4,6)
    # p1.setCellType(4,"Clue")
    # p1.setCellValue(7,3)
    # p1.setCellType(7,"Clue")
    # p1.setCellValue(15,1)
    # p1.setCellType(15,"Clue")
    # p1.setCellValue(17,8)
    # p1.setCellType(17,"Clue")
    # p1.setCellValue(20,5)
    # p1.setCellType(20,"Clue")
    # p1.setCellValue(23,8)
    # p1.setCellType(23,"Clue")
    # p1.setCellValue(27,6)
    # p1.setCellType(27,"Clue")
    # p1.setCellValue(34,8)
    # p1.setCellType(34,"Clue")
    # p1.setCellValue(35,4)
    # p1.setCellType(35,"Clue")
    # p1.setCellValue(47,8)
    # p1.setCellType(47,"Clue")
    # p1.setCellValue(48,6)
    # p1.setCellType(48,"Clue")
    # p1.setCellValue(55,3)
    # p1.setCellType(55,"Clue")
    # p1.setCellValue(59,7)
    # p1.setCellType(59,"Clue")
    # p1.setCellValue(62,2)
    # p1.setCellType(62,"Clue")
    # p1.setCellValue(65,4)
    # p1.setCellType(65,"Clue")
    # p1.setCellValue(67,1)
    # p1.setCellType(67,"Clue")
    # p1.setCellValue(75,8)
    # p1.setCellType(75,"Clue")
    # p1.setCellValue(78,3)
    # p1.setCellType(78,"Clue")
    # p1.setCellValue(79,1)
    # p1.setCellType(79,"Clue")
    # p2.addRule("thermo1","thermo",[2,12,13,5],p1)
    # p2.addRule("thermo2","thermo",[24,16,8],p1)
    # p2.addRule("thermo3","thermo",[36,44,43,33],p1)
    # p2.addRule("thermo4","thermo",[41,31,21,11],p1)
    # p2.addRule("thermo5","thermo",[41,51,61,71],p1)
    # p2.addRule("thermo6","thermo",[46,38,39,48],p1)
    # p2.addRule("thermo7","thermo",[58,66,75],p1)
    # p2.addRule("thermo8","thermo",[80,70,69,77],p1)


    app = displayApp(p1,p2)
    app.mainloop()