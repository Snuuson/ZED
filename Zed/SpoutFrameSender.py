import sys
sys.path.append('Zed/37')
import SpoutSDK
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import cv2

class SpoutFrameSender():
    def __init__(self,name="vvvvideo",width=1920,height=1080) -> None:
        self.name = name
        self.width = width
        self.height = height
        self._init_pygame()
        self._init_opengl_texture()
        self._init_sender()
        
    def _init_sender(self):
        self.spoutSender = SpoutSDK.SpoutSender()
        self.spoutSender.CreateSender(self.name, self.width, self.height, 0)

    def _init_pygame(self):
        #We use pygame to create an opengl context
        pygame.init() 
        pygame.display.set_caption('Spout Python Sender')
        pygame.display.set_mode((100,100), DOUBLEBUF|OPENGL)
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)

    def _init_opengl_texture(self):
        self.senderTextureID = glGenTextures(1)
        #initialise texture
        glBindTexture(GL_TEXTURE_2D, self.senderTextureID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # fill texture with blank data
        glCopyTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,0,0,self.width,self.height,0);
        glBindTexture(GL_TEXTURE_2D, 0)

    def SendFrame(self,frame):
        #Create byteObject from frame
        #frame = cv2.flip(frame,0)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)

        # setup frame
        glActiveTexture(GL_TEXTURE0)
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        
        #bind our senderTexture and copy the window's contents into the texture
        glBindTexture(GL_TEXTURE_2D, self.senderTextureID)

        #glCopyTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,0,0,spoutSenderWidth,spoutSenderHeight,0);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame)
        glBindTexture(GL_TEXTURE_2D, 0)

        # send texture to Spout
        # Its signature in C++ looks like this: bool SendTexture(GLuint TextureID, GLuint TextureTarget, unsigned int width, unsigned int height, bool bInvert=true, GLuint HostFBO = 0);
        self.spoutSender.SendTexture(self.senderTextureID.item(), GL_TEXTURE_2D, self.width, self.height, True, 0)