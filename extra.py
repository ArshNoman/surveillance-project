from email.mime.multipart import MIMEMultipart
from ttkthemes import themed_tk as tk
from email.mime.text import MIMEText
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import smtplib
import shutil
from tkinter import *
import os
import cv2
import pymysql
import ast
dir = 'images/5_0.jpg'
u = '1'; clss = '10C'
with open(dir, 'rb') as File:
    binary = File.read()

db = pymysql.connect(
    host="byyikg99odchbcly6vrw-mysql.services.clever-cloud.com",
    user="ubyvkstgmoy2hv2b",
    password="glxQ8H6nSNzoNROmdPqt",
    database="byyikg99odchbcly6vrw",
    autocommit=True)

cursor = db.cursor()

db.ping()  # reconnecting mysql
if cursor.connection is None:
    db.ping()

db.ping()

cursor.execute("SELECT violations FROM classes WHERE user = (%s) and name = (%s)", (u, clss))
violations = ast.literal_eval(cursor.fetchall()[0][0])
violations.append(binary)
violations = str(violations)

cursor.execute("UPDATE classes SET violations = (%s) WHERE user = (%s) and name = (%s)", (violations, u, clss))