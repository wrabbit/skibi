import struct
# $Header: /cvsroot/pyxlreader/main/OLERead.py,v 1.4 2005/11/22 22:18:06 yadra Exp $
class OLERead:
        def __init__(self):
                self.NUM_BIG_BLOCK_DEPOT_BLOCKS_POS = 0x2c
                self.SMALL_BLOCK_DEPOT_BLOCK_POS = 0x3c
                self.ROOT_START_BLOCK_POS = 0x30
                self.BIG_BLOCK_SIZE = 0x200
                self.SMALL_BLOCK_SIZE = 0x40
                self.EXTENSION_BLOCK_POS = 0x44
                self.NUM_EXTENSION_BLOCK_POS = 0x48
                self.PROPERTY_STORAGE_BLOCK_SIZE = 0x80
                self.BIG_BLOCK_DEPOT_BLOCKS_POS = 0x4c
                self.SMALL_BLOCK_THRESHOLD = 0x1000
                # property storage offsets
                self.SIZE_OF_NAME_POS = 0x40
                self.TYPE_POS = 0x42
                self.START_BLOCK_POS = 0x74
                self.SIZE_POS = 0x78
                self.IDENTIFIER_OLE = struct.pack("BBBBBBBB",0xd0,0xcf,0x11,0xe0,0xa1,0xb1,0x1a,0xe1)

                self.data=""
                
                self.props=[]

        def GetInt4d(self,data,pos):
                "some bit-wise operations"                #print "GetInt4d: %s (%s)- %s" % (pos, pos.__class__, "--")#data[pos].__class__)                ret = int(ord(data[pos]) | ord(data[pos+1]) << 8 | ord(data[pos+2]) <<16 | ord(data[pos+3]) <<24)                if ret & 0x80000000>0:                        ret = -1*(0xFFFFFFFF ^ (ret-1))                return ret
#                return int(ord(data[pos]) | ord(data[pos+1]) << 8 | ord(data[pos+2]) <<16 | ord(data[pos+3]) <<24)

        def read(self,filename):
                "reads OLE file"

                self.data = file(filename,"rb").read()

                if self.data:
                        if not self.data[:8]==self.IDENTIFIER_OLE:
                                return False

                self.numBigBlockDepotBlocks = self.GetInt4d(self.data, self.NUM_BIG_BLOCK_DEPOT_BLOCKS_POS)
                self.sbdStartBlock = self.GetInt4d(self.data, self.SMALL_BLOCK_DEPOT_BLOCK_POS)
                self.rootStartBlock = self.GetInt4d(self.data, self.ROOT_START_BLOCK_POS)
                self.extensionBlock = self.GetInt4d(self.data, self.EXTENSION_BLOCK_POS)
                self.numExtensionBlocks = self.GetInt4d(self.data, self.NUM_EXTENSION_BLOCK_POS)

                bigBlockDepotBlocks = []

                pos = self.BIG_BLOCK_DEPOT_BLOCKS_POS
                bbdBlocks = self.numBigBlockDepotBlocks
                if self.numExtensionBlocks:
                        bbdBlocks = (self.BIG_BLOCK_SIZE - self.BIG_BLOCK_DEPOT_BLOCKS_POS)/4

                for i in range(bbdBlocks):
                        bigBlockDepotBlocks.append(self.GetInt4d(self.data, pos))
                        pos +=4

                for j in range(self.numExtensionBlocks):
                        pos = (self.extensionBlock + 1) * self.BIG_BLOCK_SIZE
                        blocksToRead = min ([self.numBigBlockDepotBlocks-bbdBlocks,self.BIG_BLOCK_SIZE / 4 - 1])
                        for i in range(bbdBlocks, bbdBlocks+blocksToRead) :
                                bigBlockDepotBlocks.append(self.GetInt4d(self.data,pos))
                                pos +=4

                        bbdBlocks += blocksToRead
                        if bbdBlocks < self.numBigBlockDepotBlocks:
                                self.extensionBlock = GetInt4d(self.data, pos)

                pos = 0
                index = 0
                self.bigBlockChain = []

                for i in range( self.numBigBlockDepotBlocks):
                        pos = (bigBlockDepotBlocks[i]+1) * self.BIG_BLOCK_SIZE
                        for j in range(self.BIG_BLOCK_SIZE / 4):
                                self.bigBlockChain.append(self.GetInt4d(self.data,pos))
                                pos +=4
                                index += 1

                pos = 0
                index = 0
                sbdBlock = self.sbdStartBlock
                self.smallBlockChain = []

                while (sbdBlock != -2):
                        pos = (sbdBlock + 1) * self.BIG_BLOCK_SIZE
                        for i in range(self.BIG_BLOCK_SIZE / 4):
                                self.smallBlockChain.append(self.GetInt4d(self.data, pos))
                                pos +=4
                                index +=1
                        sbdBlock = self.bigBlockChain[sbdBlock]

                #readdata(rootStartBlock)
                block = self.rootStartBlock
                pos = 0
                self.entry = self.__readData(block)
##              print self.entry
                self.__readPropertySets()


        def __readData(self,bl):
                block = bl
                pos = 0
                data = ""
                while block != -2:
                        pos = (block + 1) * self.BIG_BLOCK_SIZE
                        data += self.data[pos:pos+self.BIG_BLOCK_SIZE]
                        block = self.bigBlockChain[block]
                return data

        def __readPropertySets(self):
                offset = 0
                while offset < len(self.entry):
                        d = self.entry[offset:offset+self.PROPERTY_STORAGE_BLOCK_SIZE]
                        nameSize = ord(d[self.SIZE_OF_NAME_POS]) | ord(d[self.SIZE_OF_NAME_POS+1]) << 8
                        Type = ord(d[self.TYPE_POS])
                        startBlock = self.GetInt4d(d, self.START_BLOCK_POS)     
                        size = self.GetInt4d(d,self.SIZE_POS)
                        name=""
                        for i in range(nameSize):
                                name += d[i]
                        name = name.replace("\x00","")
                        self.props.append({'name': name,
                                           'type': Type,
                                           'startBlock' : startBlock,
                                           'size' :size})
                        if name == "Workbook" or name == "Book":
                                self.wrkbook = len(self.props) - 1
                        if name == "Root Entry":
                                self.rootentry = len(self.props) - 1

                        offset += self.PROPERTY_STORAGE_BLOCK_SIZE;


        def getWorkBook(self):
                if self.props[self.wrkbook]['size'] < self.SMALL_BLOCK_THRESHOLD:
                        rootdata = self.__readData(self.props[self.rootentry]['startBlock'])
                        streamData = ""
                        block = self.props[self.wrkbook]['startBlock']
                        pos = 0
                        while block != -2:
                                pos = block * self.SMALL_BLOCK_SIZE
                                streamData += rootdata[pos:pos+self.SMALL_BLOCK_SIZE]
                                block = self.smallBlockChain[block]

                        return streamData
                else:
                        numBlocks = self.props[self.wrkbook]['size'] / self.BIG_BLOCK_SIZE
                        if self.props[self.wrkbook]['size'] % self.BIG_BLOCK_SIZE != 0:
                                numBlocks += 1
                        if numBlocks ==0:
                                return ""
                        streamData = ""
                        block = self.props[self.wrkbook]['startBlock']
                        pos = 0
                        while block != -2:
                                pos = (block + 1) * self.BIG_BLOCK_SIZE
                                streamData += self.data[pos:pos+self.BIG_BLOCK_SIZE]
                                block = self.bigBlockChain[block]

                        return streamData


#