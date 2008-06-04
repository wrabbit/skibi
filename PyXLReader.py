#constants# $Header: /cvsroot/pyxlreader/main/PyXLReader.py,v 1.3 2005/11/22 22:18:06 yadra Exp $
import re
import struct
import time
import string
from OLERead import OLERead

class PyXLReader:
        "main XL reader class"
        def __init__(self):
                """Constructor."""
                self.Spreadsheet_Excel_Reader_BIFF8 = 0x600
                self.Spreadsheet_Excel_Reader_BIFF7 = 0x500
                self.Spreadsheet_Excel_Reader_WorkbookGlobals = 0x5
                self.Spreadsheet_Excel_Reader_Worksheet = 0x10
                
                self.Spreadsheet_Excel_Reader_Type_BOF = 0x809
                self.Spreadsheet_Excel_Reader_Type_EOF = 0x0a
                self.Spreadsheet_Excel_Reader_Type_BOUNDSHEET = 0x85
                self.Spreadsheet_Excel_Reader_Type_DIMENSION = 0x200
                self.Spreadsheet_Excel_Reader_Type_ROW = 0x208
                self.Spreadsheet_Excel_Reader_Type_DBCELL = 0xd7
                self.Spreadsheet_Excel_Reader_Type_FILEPASS = 0x2f
                self.Spreadsheet_Excel_Reader_Type_NOTE = 0x1c
                self.Spreadsheet_Excel_Reader_Type_TXO = 0x1b6
                self.Spreadsheet_Excel_Reader_Type_RK = 0x7e
                self.Spreadsheet_Excel_Reader_Type_RK2 = 0x27e
                self.Spreadsheet_Excel_Reader_Type_MULRK = 0xbd
                self.Spreadsheet_Excel_Reader_Type_MULBLANK = 0xbe
                self.Spreadsheet_Excel_Reader_Type_INDEX = 0x20b
                self.Spreadsheet_Excel_Reader_Type_SST = 0xfc
                self.Spreadsheet_Excel_Reader_Type_EXTSST = 0xff
                self.Spreadsheet_Excel_Reader_Type_CONTINUE = 0x3c
                self.Spreadsheet_Excel_Reader_Type_LABEL = 0x204
                self.Spreadsheet_Excel_Reader_Type_LABELSST = 0xfd
                self.Spreadsheet_Excel_Reader_Type_NUMBER = 0x203
                self.Spreadsheet_Excel_Reader_Type_NAME = 0x18
                self.Spreadsheet_Excel_Reader_Type_ARRAY = 0x221
                self.Spreadsheet_Excel_Reader_Type_STRING = 0x207
                self.Spreadsheet_Excel_Reader_Type_FORMULA = 0x406
                self.Spreadsheet_Excel_Reader_Type_FORMULA2 = 0x6
                self.Spreadsheet_Excel_Reader_Type_FORMAT = 0x41e
                self.Spreadsheet_Excel_Reader_Type_XF = 0xe0
                self.Spreadsheet_Excel_Reader_Type_BOOLERR = 0x205
                self.Spreadsheet_Excel_Reader_Type_UNKNOWN = 0xffff
                self.Spreadsheet_Excel_Reader_Type_NINETEENFOUR = 0x22
                self.Spreadsheet_Excel_Reader_Type_MERGEDCELLS = 0xE5
                
                self.Spreadsheet_Excel_Reader_utcOffsetDays = 25569
                self.Spreadsheet_Excel_Reader_utcOffsetDays1904 = 24107
                self.Spreadsheet_Excel_Reader_msInADay = 24 * 60 * 60
                
                #self.Spreadsheet_Excel_Reader_DEF_NUM_FORMAT = "%.2f"
                self.Spreadsheet_Excel_Reader_DEF_NUM_FORMAT = "%s"


                self.boundsheets = []
                self.formatRecords = {}
                self.formatRecords['xfrecords']=[]
                self.sst = []
                self.sheets = {}
                self.data = ""
                self.pos = ""
#               self._ole = ""
                self._defaultEncoding = ""
                self._defaultFormat = self.Spreadsheet_Excel_Reader_DEF_NUM_FORMAT
                self._columnsFormat = []
                self._rowoffset = 1
                self._coloffset = 1

                self.dateFormats = {
                0xe : "d/m/Y",
                0xf : "d-M-Y",
                0x10 : "d-M",
                0x11 : "M-Y",
                0x12 : "h:i a",
                0x13 : "h:i:s a",
                0x14 : "H:i",
                0x15 : "H:i:s",
                0x16 : "d/m/Y H:i",
                0x2d : "i:s",
                0x2e : "H:i:s",
                0x2f : "i:s.S"}

                self.numberFormats = {
                0x1 : "%1.0f",   # "0"
                0x2 : "%1.2f",   # "0.00",
                0x3 : "%1.0f",   # "#,##0",
                0x4 : "%1.2f",   # "#,##0.00",
                0x5 : "%1.0f",   # "$#,##0;($#,##0)"
                0x6 : '$%1.0f',  # "$#,##0;($#,##0)"
                0x7 : '$%1.2f',  # "$#,##0.00;($#,##0.00)",
                0x8 : '$%1.2f',  # "$#,##0.00;($#,##0.00)",
                0x9 : '%1.0f%%', #  "0%"
                0xa : '%1.2f%%', #  "0.00%"
                0xb : '%1.2f',   # 0.00E00",
                0x25 : '%1.0f',  # "#,##0;(#,##0)",
                0x26 : '%1.0f',  # "#,##0;(#,##0)",
                0x27 : '%1.2f',  # "#,##0.00;(#,##0.00)",
                0x28 : '%1.2f',  # "#,##0.00;(#,##0.00)",
                0x29 : '%1.0f',  # "#,##0;(#,##0)",
                0x2a : '$%1.0f', # "$#,##0;($#,##0)",
                0x2b : '%1.2f',  # "#,##0.00;(#,##0.00)",
                0x2c : '$%1.2f', # "$#,##0.00;($#,##0.00)",
                0x30 : '%1.0f'}; # "##0.0E0";

                self._ole = OLERead()

        def setOutputEncoding(self, encoding):
                self._defaultEncoding=encoding

        def setRowColOffset(self, iOffset):
                self._rowoffset = iOffset
                self._coloffset = iOffset

        def setDefaultFormat(self, sFormat):
                self._defaultFormat = sFormat

        def setColumnFormat (self, column, sFormat):
                self._columnsFormat[column] = sFormat

        def read(self,sFileName):
                "Read data from fileName"
                self._ole.read(sFileName)
                self.data=self._ole.getWorkBook()
                self.pos = 0
                self._parse()


#
#    function _parse(){
        def _parse(self):
                formatstr = False
                opcode = ""
                conlength = ""
                pos = 0
                formattingRuns = ""
                extendedRunLength = ""

                code = ord(self.data[pos]) | ord(self.data[pos+1]) << 8
                length = ord(self.data[pos+2]) | ord(self.data[pos+3]) <<8
                version = ord(self.data[pos+4]) | ord(self.data[pos+5]) <<8

                substreamType = ord(self.data[pos+6]) | ord(self.data[pos+7]) << 8
                if version != self.Spreadsheet_Excel_Reader_BIFF8 and self.Spreadsheet_Excel_Reader_BIFF7:
                        return False
                if substreamType != self.Spreadsheet_Excel_Reader_WorkbookGlobals:
                        return False
                pos += length + 4
                code = ord(self.data[pos]) | ord(self.data[pos+1]) << 8
                length = ord(self.data[pos+2]) | ord(self.data[pos+3]) <<8
                while code != self.Spreadsheet_Excel_Reader_Type_EOF:
                        if code == self.Spreadsheet_Excel_Reader_Type_SST:
                                spos = pos + 4
                                limitpos = spos + length
                                uniqueStrings = self._GetInt4d(self.data, spos+4)
                                spos += 8;
                                for i in range(uniqueStrings):
                                        if spos == limitpos:
                                                opcode = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                                conlength = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                                if opcode != 0x3c:
                                                        return -1
                                                pos += 4
                                                limitpos = spos + conlength
                                        numChars = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                        spos += 2
                                        optionFlags = ord(self.data[spos])
                                        spos+=1
                                        asciiEncoding = ((optionFlags & 0x01) == 0)
                                        extendedString = ( (optionFlags & 0x04) != 0)
                                        # See if string contains formatting information
                                        richString = ( (optionFlags & 0x08) != 0)
                                        if richString:
                                                # Read in the crun
                                                formattingRuns = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                                spos += 2;
                                        if extendedString:
                                                # Read in cchExtRst
                                                extendedRunLength = self._GetInt4d(self.data, spos)
                                                spos += 4
                                        #ascii or not
                                        if asciiEncoding:
                                                charlen = numChars
                                        else:
                                                charlen = numChars * 2

                                        if spos + charlen < limitpos:
                                                retstr = self.data[spos:spos+charlen]
                                                spos += charlen
                                        else:
                                                # found countinue
                                                retstr = self.data[spos:limitpos]
                                                bytesRead = limitpos - spos
                                                if asciiEncoding:
                                                        minus = bytesRead
                                                else:
                                                        minus = bytesRead / 2
                                                charsLeft = numChars - minus
                                                spos = limitpos

                                                while charsLeft > 0:
                                                        opcode = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                                        conlength = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                                        if opcode != 0x3c:
                                                                return -1;

                                                        spos += 4
                                                        limitpos = spos + conlength
                                                        option = ord(self.data[spos])
                                                        spos += 1
                                                        if asciiEncoding and (option == 0) :
                                                                charlen = min([charsLeft, limitpos - spos]) # min(charsLeft, conlength);
                                                                retstr += self.data[spos:spos+charlen]
                                                                charsLeft -= charlen
                                                                asciiEncoding = True
                                                        elif not asciiEncoding and (option != 0):
                                                                charlen = min([charsLeft * 2, limitpos - spos]) # min(charsLeft, conlength);
                                                                retstr += self.data[spos, spos+charlen]
                                                                charsLeft -= charlen/2
                                                                asciiEncoding = False
                                                        elif not asciiEncoding and (option == 0):
                                                                # Bummer - the string starts off as Unicode, but after the
                                                                # continuation it is in straightforward ASCII encoding
                                                                charlen = min([charsLeft, limitpos - spos]) # min(charsLeft, conlength);
                                                                for j in range(charlen):
                                                                        retstr += self.data[spos + j].chr(0)

                                                                charsLeft -= charlen;
                                                                asciiEncoding = False;
                                                        else:
                                                                newstr = '';
                                                                for j in range(len(retstr)):
                                                                      newstr = retstr[j].chr(0)#+=
                                                                retstr = newstr
                                                                charlen = min([charsLeft * 2, limitpos - spos]) # min(charsLeft, conlength);
                                                                retstr += self.data[spos:spos+charlen]
                                                                charsLeft -= charlen/2;
                                                                asciiEncoding = False
                                                                #echo "Izavrat\n";
                                                                  
                                                        spos += charlen;

#                                                       print "FCUK"
#                                                       for i in [opcode,conlength,spos,limitpos,option,charlen,retstr,charsLeft,asciiEncoding,newstr]:
#                                                               print i 
#                                       print asciiEncoding
                                        if asciiEncoding:
                                                pass
#                                               print ord(retstr[0])
                                        else:
                                                retstr=retstr.decode("utf_16_le")
                                                print retstr
                                        if richString:
                                                  spos += 4 * formattingRuns
                                        # For extended strings, skip over the extended string data
                                        if extendedString:
                                                  spos += extendedRunLength
                                        self.sst.append(retstr)




                        elif code == self.Spreadsheet_Excel_Reader_Type_FILEPASS:
                                return False
                                pass

                        elif code == self.Spreadsheet_Excel_Reader_Type_NAME:
                                pass

                        elif code == self.Spreadsheet_Excel_Reader_Type_FORMAT:
                                indexCode = ord(self.data[pos+4]) | ord(self.data[pos+5]) << 8
                                if version == self.Spreadsheet_Excel_Reader_BIFF8:
                                        numchars = ord(self.data[pos+6]) | ord(self.data[pos+7]) << 8
                                        if ord(self.data[pos+8]) == 0:
                                                formatString = self.data[pos+9:pos+9+numchars]
                                        else:
                                                formatString = self.data[pos+9:pos+9+numchars*2]
                                else:
                                        numchars = ord(self.data[pos+6])
                                        formatString = self.data[pos+7:pos+7+numchars*2]
                                self.formatRecords[indexCode] = formatString

                        elif code == self.Spreadsheet_Excel_Reader_Type_XF:
                                indexCode = ord(self.data[pos+6]) | ord(self.data[pos+7]) << 8
#                               print indexCode
#                               print self.dateFormats
                                if not self.formatRecords.has_key('xfrecords'):
                                        self.formatRecords['xfrecords']=[]
                                if self.dateFormats.has_key(indexCode):
#                                       print self.dateFormats[indexCode]
                                        self.formatRecords['xfrecords'].append({'type' : 'date', 'format' : self.dateFormats[indexCode]})
                                elif self.numberFormats.has_key(indexCode):
#                                       print "isnumber "+self.numberFormats[indexCode]
                                        self.formatRecords['xfrecords'].append({'type':'number', 'format' : self.numberFormats[indexCode]})
                                else:
                                        isdate=False
                                        if indexCode > 0:
                                                if self.formatRecords.has_key(indexCode):
                                                        formatstr = self.formatRecords[indexCode]

                                                if 0:
                                                        print "PREG";
                                                        isdate = True
#                                                       if re.match("/[^hmsday\/\-:\s]/i", formatstr)
                                                        formatstr.replace('mm','i')
                                                        formatstr.replace('h','H')
                                        if isdate:
                                                self.formatRecords['xfrecords'].append({'type' : 'date', 'format' : formatstr})
                                        else:
                                                self.formatRecords['xfrecords'].append({'type' : 'other', 'format' : '', 'code' : indexCode})



                        elif code == self.Spreadsheet_Excel_Reader_Type_NINETEENFOUR:
                                self.nineteenFour = (ord(self.data[pos+4]) == 1)

                        elif code == self.Spreadsheet_Excel_Reader_Type_BOUNDSHEET:
                                rec_offset = self._GetInt4d(self.data, pos+4)
                                rec_typeFlag = ord(self.data[pos+8])
                                rec_visibilityFlag = ord(self.data[pos+9])
                                rec_length = ord (self.data[pos+10])
                                if version == self.Spreadsheet_Excel_Reader_BIFF8:
                                        chartype = ord(self.data[pos+11])         
                                        if chartype ==0:                          
                                                rec_name = self.data[pos+12:pos+12+rec_length]
                                        else:
                                                rec_name = self.data[pos+12:pos+12+rec_length]
#                                               rec_name = self._encodeUTF16(self.data[pos+12:pos+12+(rec_length*2)])

                                elif version == self.Spreadsheet_Excel_Reader_BIFF7:
                                        rec_name = self.data[pos+11:pos+11+rec_length]
                                self.boundsheets.append({'name' : rec_name, 'offset' : rec_offset})



                        pos += length +4
                        code = ord(self.data[pos]) | ord(self.data[pos+1]) << 8
                        length = ord(self.data[pos+2]) | ord (self.data[pos+3]) <<8
                        
#               for i in self.formatRecords['xfrecords']:
#                       print i
                for key in range(len(self.boundsheets)):
                        value = self.boundsheets[key]
                        self.sn = key
                        self._parsesheet(value['offset'])
                return True

        def _parsesheet(self,spos):
                cont = True
                code = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                length = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8

                version = ord(self.data[spos + 4]) | ord(self.data[spos + 5]) << 8
                substreamType = ord(self.data[spos + 6]) | ord(self.data[spos + 7]) << 8

                if (version != self.Spreadsheet_Excel_Reader_BIFF8) and (version != self.Spreadsheet_Excel_Reader_BIFF7):
                        return -1

                if substreamType != self.Spreadsheet_Excel_Reader_Worksheet:
                        return -2

                spos += length + 4


                if not self.sheets.has_key(self.sn):
                        self.sheets[self.sn]={}
                self.sheets[self.sn]['maxrow'] = self._rowoffset - 1
                self.sheets[self.sn]['maxcol'] = self._coloffset - 1
                self.sheets[self.sn]['cellsInfo']={}#y
                
                while cont:
                        lowcode = ord(self.data[spos])
                        if lowcode == self.Spreadsheet_Excel_Reader_Type_EOF:
                                break
                        code = lowcode | ord(self.data[spos+1]) << 8
                        length = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                        spos += 4
                        self.multiplier = 1 # need for format with %

                        if code == self.Spreadsheet_Excel_Reader_Type_DIMENSION:
                                if not hasattr(self,"numRows"):
                                        if (length == 10) or (version == self.Spreadsheet_Excel_Reader_BIFF7):
                                                self.sheets[self.sn]['numRows'] = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                                self.sheets[self.sn]['numCols'] = ord(self.data[spos+6]) | ord(self.data[spos+7]) << 8
                                        else :
                                                self.sheets[self.sn]['numRows'] = ord(self.data[spos+4]) | ord(self.data[spos+5]) << 8
                                                self.sheets[self.sn]['numCols'] = ord(self.data[spos+10]) | ord(self.data[spos+11]) << 8


                        elif code == self.Spreadsheet_Excel_Reader_Type_MERGEDCELLS:
                                cellRanges = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                for i in range(cellRanges):
                                        fr =  ord(self.data[spos + 8*i + 2]) | ord(self.data[spos + 8*i + 3]) << 8
                                        lr =  ord(self.data[spos + 8*i + 4]) | ord(self.data[spos + 8*i + 5]) << 8
                                        fc =  ord(self.data[spos + 8*i + 6]) | ord(self.data[spos + 8*i + 7]) << 8
                                        lc =  ord(self.data[spos + 8*i + 8]) | ord(self.data[spos + 8*i + 9]) << 8

                                        if lr - fr > 0:
                                                pass
                                                print "lr - fr"
#                                               self.sheets[self.sn]['cellsInfo'][fr+1][fc+1]['rowspan'] = lr - fr + 1
                                        if lc - fc > 0 :
                                                pass
                                                print "lc - fc"
#                                               self.sheets[self.sn]['cellsInfo'][fr+1][fc+1]['colspan'] = lc - fc + 1


                        elif code == self.Spreadsheet_Excel_Reader_Type_RK2:
#                               print "Spreadsheet_Excel_Reader_Type_RK"
                                row = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                rknum = self._GetInt4d(self.data, spos + 6)
                                numValue = self._GetIEEE754(rknum)

                                if self.isDate(spos):
                                        self.createDate(numValue)
#                                       String, raw = self.createDate(numValue)
                                else:
                                        raw = numValue
#                                       if isset($this->_columnsFormat[$column + 1]):
#                                               $this->curformat = $this->_columnsFormat[$column + 1]
                                        if len(self._columnsFormat) > column:
                                                self.curformat = self._columnsFormat[column+1]
#                                       $string = sprintf($this->curformat, $numValue * $this->multiplier)
                                        String = self.curformat % (numValue * self.multiplier)
#                                       print String
                                self.addcell(row, column, String, raw)

                        elif code == self.Spreadsheet_Excel_Reader_Type_LABELSST:
                                row        = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column     = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                xfindex    = ord(self.data[spos+4]) | ord(self.data[spos+5]) << 8
                                index  = self._GetInt4d(self.data, spos + 6)
                                #var_dump($this->sst);
                                self.addcell(row, column, self.sst[index])
                                #//echo "LabelSST $row $column $string\n";

                        elif code == self.Spreadsheet_Excel_Reader_Type_MULRK:
                                row        = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                colFirst   = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                colLast    = ord(self.data[spos + length - 2]) | ord(self.data[spos + length - 1]) << 8
                                columns    = colLast - colFirst + 1
                                tmppos = spos+4

                                for i in range(columns):
                                        numValue = self._GetIEEE754(self._GetInt4d(self.data, tmppos + 2))
                                        if self.isDate(tmppos-4):
                                                print "FCUKDATE!";
#                                               list(String, raw) = self.createDate(numValue)
                                        else:
                                                raw = numValue
                                                if len(self._columnsFormat) > colFirst + i + 1:
                                                        print "FCUKCOL!";
                                                        self.curformat = self._columnsFormat[colFirst + i + 1]

                                        String = self.curformat % (numValue * self.multiplier)
                                        
                                        #$rec['rknumbers'][$i]['xfindex'] = ord($rec['data'][$pos]) | ord($rec['data'][$pos+1]) << 8;
                                        tmppos += 6;
                                        self.addcell(row, colFirst + i, String, raw)
                                        #echo "MULRK $row ".($colFirst + $i)." $string\n";
                                #MulRKRecord($r);
                                #Get the individual cell records from the multiple record
                                #$num = ;
                        elif code == self.Spreadsheet_Excel_Reader_Type_NUMBER:
                                row    = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                tmp={}
                                tmp['double'] = struct.unpack("d", self.data[spos + 6:spos + 14]) 

#                               print tmp
                                if self.isDate(spos):
                                        String, raw = self.createDate(tmp['double'][0])
                                else:
                                        if len(self._columnsFormat) > column + 1:
                                                self.curformat = self._columnsFormat[column + 1]
                                        raw = self.createNumber(spos)
                                        String = self.curformat % (raw * self.multiplier)
#                                       print String
                                self.addcell(row, column, String, raw)

                        elif code == self.Spreadsheet_Excel_Reader_Type_FORMULA2:
                                row    = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                if (ord(self.data[spos+6])==0) and (ord(self.data[spos+12])==255) and (ord(self.data[spos+13])==255) :
                                        pass
                                        #String formula. Result follows in a STRING record
                                        #//echo "FORMULA $row $column Formula with a string<br>\n";
                                elif (ord(self.data[spos+6])==1) and (ord(self.data[spos+12])==255) and (ord(self.data[spos+13])==255):
                                        pass
                                        #//Boolean formula. Result is in +2; 0=False,1=True
                                elif (ord(self.data[spos+6])==2) and (ord(self.data[spos+12])==255) and (ord(self.data[spos+13])==255):
                                        pass
                                        #//Error formula. Error code is in +2;
                                elif (ord(self.data[spos+6])==3) and (ord(self.data[spos+12])==255) and (ord(self.data[spos+13])==255):
                                        pass
                                        #//Formula result is a null string.
                                else:
                                        #// result is a number, so first 14 bytes are just like a _NUMBER record
                                        tmp = struct.unpack("d", self.data[spos + 6: spos + 6 + 8]) # // It machine machine dependent
                                        if self.isDate(spos):
                                                String, raw = self.createDate(tmp[0])
                                        else:
                                                if len(self._columnsFormat) > column + 1:
                                                        self.curformat = self._columnsFormat[column + 1]

                                        raw = self.createNumber(spos)
                                        String = self.curformat % (raw * self.multiplier)
                                        #$this->addcell(DateRecord($r, 1));
                                self.addcell(row, column, String, raw)

                        elif code == self.Spreadsheet_Excel_Reader_Type_BOOLERR:
                                row    = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                String = ord(self.data[spos+6])
                                self.addcell(row, column, String)
                        elif code == self.Spreadsheet_Excel_Reader_Type_ROW:
                                pass
                        elif code == self.Spreadsheet_Excel_Reader_Type_DBCELL:
                                pass
                        elif code == self.Spreadsheet_Excel_Reader_Type_MULBLANK:
                                pass
                        elif code == self.Spreadsheet_Excel_Reader_Type_LABEL:
                                row    = ord(self.data[spos]) | ord(self.data[spos+1]) << 8
                                column = ord(self.data[spos+2]) | ord(self.data[spos+3]) << 8
                                numchars = ord(self.data[spos + 6]) | ord(self.data[spos + 7]) << 8
                                String=self.data[spos + 8: spos + 8 + numchars]
                                self.addcell(row, column, String)

                                #// $this->addcell(LabelRecord($r));
                        elif code == self.Spreadsheet_Excel_Reader_Type_EOF:
                                cont = False

                        spos += length


#               print self.sheets
                if not self.sheets[self.sn].has_key('numRows'):
                        self.sheets[self.sn]['numRows'] = self.sheets[self.sn]['maxrow']
                if not self.sheets[self.sn].has_key('numCols'):
                        self.sheets[self.sn]['numCols'] = self.sheets[self.sn]['maxcol']


        def isDate(self,spos):
                #$xfindex = GetInt2d(, 4);
                xfindex = ord(self.data[spos+4]) | ord(self.data[spos+5]) << 8
                #echo 'check is date '.$xfindex.' '.$this->formatRecords['xfrecords'][$xfindex]['type']."\n";
                #var_dump($this->formatRecords['xfrecords'][$xfindex]);
#               print(self.formatRecords['xfrecords'][xfindex])
                if (self.formatRecords['xfrecords'][xfindex]['type'] == 'date') :
                        self.curformat = self.formatRecords['xfrecords'][xfindex]['format']
                        self.rectype = 'date'
#                       for i in [xfindex,self.curformat,self.rectype]:
#                               print i
                        return True;
                else:
                        if (self.formatRecords['xfrecords'][xfindex]['type'] == 'number') :
                                self.curformat = self.formatRecords['xfrecords'][xfindex]['format']
                                self.rectype = 'number'
                                if (xfindex == 0x9) or (xfindex == 0xa):
                                        self.multiplier = 100
                        else:
                                self.curformat = self._defaultFormat
                                self.rectype = 'unknown'
                        return False

        

        def createDate(self,numValue):
                if numValue > 1:
                        if self.nineteenFour:
                                minus = self.Spreadsheet_Excel_Reader_utcOffsetDays1904;
                        else:
                                minus = self.Spreadsheet_Excel_Reader_utcOffsetDays     
                        utcDays = numValue - minus
                        utcValue = int(round(utcDays * self.Spreadsheet_Excel_Reader_msInADay))
                        String = self.date (self.curformat, utcValue);
                        raw = utcValue
                else:
                        raw = numValue
                        hours = floor(numValue * 24)
                        mins = floor(numValue * 24 * 60) - hours * 60
                        secs = floor(numValue * self.Spreadsheet_Excel_Reader_msInADay) - hours * 60 * 60 - mins * 60
                        String = self.date (self.curformat, time.mktime([hours, mins, secs]))
                return [String, raw]

#
        def createNumber(self,spos):
                rknumhigh = self._GetInt4d(self.data, spos + 10)
                rknumlow = self._GetInt4d(self.data, spos + 6)
                sign = (rknumhigh & 0x80000000) >> 31
                exp =  (rknumhigh & 0x7ff00000) >> 20

                mantissa = (0x100000 | (rknumhigh & 0x000fffff))
                mantissalow1 = (rknumlow & 0x80000000) >> 31
                mantissalow2 = (rknumlow & 0x7fffffff)
                value = float(mantissa) / float(pow( 2 , (20- (exp - 1023))))
#               print value
                if mantissalow1 != 0:
                        value += 1 / pow (2 , (21 - (exp - 1023)))
                value += mantissalow2 / pow (2 , (52 - (exp - 1023)))
                #echo "Sign = $sign, Exp = $exp, mantissahighx = $mantissa, mantissalow1 = $mantissalow1, mantissalow2 = $mantissalow2<br>\n"
                if (sign) :
                        value = -1 * value;
                return  value;
#
        def addcell(self, row, col, String, raw = ''):
                #echo "ADD cel $row-$col $string\n";
                self.sheets[self.sn]['maxrow'] = max([self.sheets[self.sn]['maxrow'], row + self._rowoffset])
                self.sheets[self.sn]['maxcol'] = max([self.sheets[self.sn]['maxcol'], col + self._coloffset])

                if not self.sheets[self.sn].has_key("cells"):
                        self.sheets[self.sn]['cells']={}

                if not self.sheets[self.sn]['cells'].has_key(row + self._rowoffset):
                        self.sheets[self.sn]['cells'][row + self._rowoffset]={}

                self.sheets[self.sn]['cells'][row + self._rowoffset][col + self._coloffset] = String

                if raw or hasattr(self,"rectype"):
                        if not self.sheets[self.sn]['cellsInfo'].has_key(row + self._rowoffset):
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset]={}
                        if not self.sheets[self.sn]['cellsInfo'][row + self._rowoffset].has_key(col + self._coloffset):
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset][col + self._coloffset]={}

                        if (raw):
#                               print "RAW!"
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset][col + self._coloffset]={}
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset][col + self._coloffset]['raw'] = raw
                        if hasattr(self,"rectype"):
#                               print "rectype"
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset][col + self._coloffset]={}
                                self.sheets[self.sn]['cellsInfo'][row + self._rowoffset][col + self._coloffset]['type'] = self.rectype
        #               print self.sheets

    
#
#
        def _GetIEEE754(self,rknum):
                if (rknum & 0x02) != 0:
                        value = rknum >> 2
                else :
# mmp
# first comment out the previously existing 7 lines of code here
#                      tmp = struct.unpack("d", struct.pack("VV", 0, (rknum & 0xfffffffc)))
#                       #value = tmp[''];
#                       if tmp.has_key(1):
#                           value = tmp[1]
#                       else :
#                           value = tmp['']
# I got my info on IEEE754 encoding from 
# http://research.microsoft.com/~hollasch/cgindex/coding/ieeefloat.html
# The RK format calls for using only the most significant 30 bits of the
# 64 bit floating point value. The other 34 bits are assumed to be 0
# / So, we use the upper 30 bits of $rknum as follows...
                        sign = (rknum & 0x80000000) >> 31
                        exp = (rknum & 0x7ff00000) >> 20
                        mantissa = (0x100000 | (rknum & 0x000ffffc))
                        value = mantissa / pow( 2 , (20- (exp - 1023)))
                        if (sign):
                                value = -1 * value;
#end of changes by mmp          



                if ((rknum & 0x01) != 0):
                        value /= 100
                return value;

        def _GetInt4d(self,data,pos):
                "some bit-wise operations"
                return ord(data[pos]) | ord(data[pos+1]) << 8 | ord(data[pos+2]) <<16 | ord(data[pos+3]) <<24

        def date(self, format, utcValue):
                j=""
                for letter in format.replace("i","M"):
                        if letter in string.ascii_letters :
                                j+="%"+letter
                        else:
                                j+=letter
                format = j
                return time.strftime(format,time.localtime(utcValue))
