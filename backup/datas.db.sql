BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "settings" (
	"defaultHourNotification"	INTEGER,
	"maxStudyHour"	INTEGER,
	"studyDays"	TEXT(7),
	"minimumDuration"	INTEGER,
	"hourStartDay"	INTEGER,
	"hourEndDay"	INTEGER
);
CREATE TABLE IF NOT EXISTS "calendar" (
	"ID"	INTEGER NOT NULL,
	"title"	TEXT(20) NOT NULL,
	"notes"	TEXT,
	"description"	TEXT,
	"weekReps"	TEXT(7) DEFAULT 0000000,
	"insertedDay"	TEXT(10) NOT NULL,
	"arrExceptions"	TEXT,
	"startDate"	TEXT(10) NOT NULL,
	"endDate"	TEXT(10),
	"timeStartDate"	TEXT(5),
	"timeEndDate"	TEXT(5),
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "flashcards" (
	"ID"	INTEGER NOT NULL,
	"front"	TEXT NOT NULL,
	"back"	TEXT,
	"deadline"	TEXT(10),
	"box"	INTEGER(2) NOT NULL,
	"sourceID"	INTEGER NOT NULL,
	"filenameScheme"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sources" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"numberPages"	INTEGER(5) NOT NULL,
	"studiedPages"	INTEGER(5),
	"filename"	TEXT,
	"deadline"	TEXT(10),
	"arrSessions"	TEXT,
	"url"	TEXT,
	"durationMinutes"	INTEGER,
	"viewedMinutes"	INTEGER,
	"insertDate"	TEXT(10) NOT NULL,
	"type"	TEXT,
	"jsonDateStudyPages"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT INTO "settings" VALUES (15,8,'0111000',5,7,22);
INSERT INTO "calendar" VALUES (1,'prova2','Questa è una nota di prova','prova','0000000','2023-08-16','{}','2023-08-16','2023-09-02','08:00','09:00');
INSERT INTO "calendar" VALUES (2,'prova1','Questa è una nota ripetitiva di prova','prova','1000000','2023-09-02','{}','2023-09-02',NULL,'09:45','10:00');
INSERT INTO "calendar" VALUES (3,'prova3','Questa è una nota di prova lunga','prova','0000000','2023-09-02','{}','2023-09-02','2023-09-05','10:30','11:00');
INSERT INTO "flashcards" VALUES (0,'GOTA[latex]\frac{a}{b}[/latex]','GO[latex][/latex]AT','2023-09-10',0,0,'/home/cristian/Pictures/pT7r5aK6c.png');
INSERT INTO "flashcards" VALUES (2,'Fucile','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum tortor libero, auctor vel enim non, dapibus dignissim erat. Nulla sed venenatis mauris, a mollis mauris. Vestibulum sodales nec nibh id faucibus. Sed rhoncus lacus id justo hendrerit, eu sagittis sapien imperdiet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec ultrices vel tortor at feugiat. Sed interdum est urna. Vivamus pharetra eleifend dolor a iaculis. Pellentesque faucibus sodales tempor. Integer sit amet urna varius, hendrerit nulla nec, finibus massa. Phasellus faucibus iaculis orci ac laoreet. Aliquam auctor, tortor eu aliquam ultrices, lectus metus sollicitudin augue, ac tincidunt lectus nisi eget quam. Etiam molestie magna nec eros mattis dignissim.



Integer vestibulum dui sit amet gravida faucibus. Mauris tristique leo dui, vitae faucibus sem commodo in. Quisque sit amet gravida dui, non hendrerit leo. Quisque elit est, scelerisque a nulla ut, tempor interdum nunc. Ut mollis dictum ullamcorper. Praesent mattis erat a risus rutrum, vel condimentum orci eleifend. Vivamus arcu mi, porta non luctus sit amet, lobortis vitae sem. Ut molestie at neque a porta. Nam in risus facilisis, mattis metus sed, euismod orci. In vitae ex non ante blandit euismod. Suspendisse convallis euismod dolor, in cursus nibh tempor a.

Donec dolor elit, volutpat sed posuere ut, ultricies sit amet lorem. Fusce ullamcorper bibendum lectus, et aliquam diam pharetra vel. Aenean ipsum magna, eleifend non dignissim vel, mollis ut ligula. Nullam ornare, diam nec lobortis cursus, arcu orci commodo est, ut laoreet eros ex eu odio. Mauris congue purus eros, vitae vehicula mi tincidunt vel. Aliquam quis magna dolor. Duis id erat a turpis dictum pellentesque ac quis mauris. Aenean sit amet pellentesque urna. Donec tincidunt leo in lorem dignissim, vel consequat sapien condimentum. Mauris in eleifend lectus. In euismod tristique tellus, a pharetra leo vestibulum et.

Nulla lectus libero, rhoncus vitae pellentesque nec, lobortis ac massa. Nam iaculis, nisl ornare suscipit ornare, ante leo tincidunt ex, ut maximus nunc lacus ut odio. Praesent eleifend maximus lacus, sed interdum ligula mattis a. Ut aliquet, ante eu pellentesque auctor, magna felis posuere metus, in faucibus lorem justo id sem. Duis vel tortor enim. Proin in est ut ante pulvinar fermentum. Aenean quis dictum nisi, a accumsan diam. Aenean facilisis auctor augue, quis aliquam purus dictum eu. Duis elementum venenatis aliquet. Donec ut nunc vel risus posuere commodo eget nec quam. Phasellus pellentesque rutrum odio, et efficitur turpis blandit eget. Ut non justo velit.

Nullam sem sem, gravida sit amet commodo at, pharetra ac risus. Aliquam erat volutpat. Vestibulum sit amet est auctor, rhoncus lectus in, sagittis leo. Nunc rutrum elit a ex bibendum mollis. Donec sagittis nisl mauris, eu cursus risus lobortis sit amet. Nam fringilla leo et nulla dictum dictum. Vivamus ac velit posuere, tempus urna quis, sagittis lorem. Mauris pellentesque aliquam risus, et laoreet eros congue id. Vivamus sit amet ex euismod, efficitur nibh vitae, mattis erat. Pellentesque rhoncus eros ut tellus porttitor, vel ornare justo imperdiet. Aliquam et ornare mauris. Sed lorem justo, molestie rhoncus nisl nec, ultricies tristique metus. In molestie est nunc, non facilisis tellus laoreet quis. Integer rhoncus, lacus vitae congue pretium, metus massa aliquet metus, vitae varius massa nisl vitae risus. Ut molestie sodales dignissim. Etiam varius scelerisque eros, eu tristique augue congue in.

Proin ullamcorper orci nulla, vulputate pretium magna cursus in. Donec maximus, augue id varius vehicula, diam est ultricies tortor, id semper mauris mauris in quam. Nullam sem elit, tempor eget aliquet sit amet, dapibus non velit. Etiam quis ante luctus, sagittis ex quis, tincidunt mi. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut mattis tincidunt turpis quis sollicitudin. Quisque sollicitudin ex ac velit gravida varius. Morbi ac accumsan nulla. Aliquam faucibus sapien ut mattis volutpat. Cras interdum neque enim, at consectetur ipsum pellentesque sed. Maecenas molestie gravida mollis. Pellentesque dictum convallis mi, non faucibus ligula. Curabitur consectetur turpis in sapien auctor tincidunt. Phasellus molestie faucibus diam, vel molestie justo pulvinar rutrum. Etiam vel nisi ullamcorper orci iaculis vestibulum eget eget dui. Vivamus tincidunt, mi in facilisis varius, ex lorem fermentum risus, vitae fringilla sapien nulla eget urna.

Quisque vulputate finibus mi, vel placerat ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec id mauris ut augue laoreet cursus. Pellentesque hendrerit ex nec nunc malesuada fringilla quis placerat risus. Vivamus euismod hendrerit ex eget laoreet. Aliquam in mauris ligula. Nunc quis scelerisque ante. Morbi condimentum nunc nec purus aliquet, ac sodales quam dictum. Morbi ipsum quam, aliquam sit amet porttitor et, ultrices nec eros.

Donec quis lectus rhoncus, rhoncus augue non, scelerisque lorem. In non porta sapien. Vestibulum at sodales elit. Pellentesque venenatis eu metus ut aliquam. Morbi pulvinar neque ut eros rhoncus facilisis. Praesent at convallis lacus. Mauris vehicula, nunc in interdum ultricies, quam ex convallis leo, eu tincidunt sem tellus id magna. Cras venenatis lobortis rutrum. Proin porta aliquet finibus. Nulla vehicula volutpat dolor, ut iaculis turpis cursus ut. Vivamus vehicula tempor auctor.

Donec porttitor maximus urna, quis tincidunt est vehicula at. Proin suscipit eu leo a ullamcorper. Donec et aliquam nunc. Sed rhoncus nisl pharetra, semper metus nec, laoreet turpis. Morbi interdum ligula ac egestas elementum. Nam mauris felis, vestibulum nec eros vel, lacinia accumsan nisl. Nam ut nisi odio. Ut lobortis, mauris posuere elementum convallis, ipsum nibh auctor neque, eu maximus nisi nibh vel neque. Ut euismod purus ac molestie elementum. Curabitur in nunc ipsum. Proin pharetra maximus ante quis aliquam.

Maecenas efficitur tristique ex, ut gravida arcu volutpat a. Nulla a tortor at neque dapibus gravida id quis augue. Pellentesque cursus felis faucibus posuere pellentesque. Nulla tempor venenatis imperdiet. Etiam eu tortor in turpis cursus rhoncus vitae nec odio. Curabitur vitae sapien turpis. Donec consequat lorem ex, a sollicitudin risus tristique eget. Nunc nec ultrices nulla, non laoreet nulla.

Quisque tincidunt tortor sit amet vulputate fringilla. Morbi et erat ex. Fusce gravida nisl ut purus condimentum feugiat. Nulla tempus sodales odio. Cras at.
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum tortor libero, auctor vel enim non, dapibus dignissim erat. Nulla sed venenatis mauris, a mollis mauris. Vestibulum sodales nec nibh id faucibus. Sed rhoncus lacus id justo hendrerit, eu sagittis sapien imperdiet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Donec ultrices vel tortor at feugiat. Sed interdum est urna. Vivamus pharetra eleifend dolor a iaculis. Pellentesque faucibus sodales tempor. Integer sit amet urna varius, hendrerit nulla nec, finibus massa. Phasellus faucibus iaculis orci ac laoreet. Aliquam auctor, tortor eu aliquam ultrices, lectus metus sollicitudin augue, ac tincidunt lectus nisi eget quam. Etiam molestie magna nec eros mattis dignissim.

Integer vestibulum dui sit amet gravida faucibus. Mauris tristique leo dui, vitae faucibus sem commodo in. Quisque sit amet gravida dui, non hendrerit leo. Quisque elit est, scelerisque a nulla ut, tempor interdum nunc. Ut mollis dictum ullamcorper. Praesent mattis erat a risus rutrum, vel condimentum orci eleifend. Vivamus arcu mi, porta non luctus sit amet, lobortis vitae sem. Ut molestie at neque a porta. Nam in risus facilisis, mattis metus sed, euismod orci. In vitae ex non ante blandit euismod. Suspendisse convallis euismod dolor, in cursus nibh tempor a.

Donec dolor elit, volutpat sed posuere ut, ultricies sit amet lorem. Fusce ullamcorper bibendum lectus, et aliquam diam pharetra vel. Aenean ipsum magna, eleifend non dignissim vel, mollis ut ligula. Nullam ornare, diam nec lobortis cursus, arcu orci commodo est, ut laoreet eros ex eu odio. Mauris congue purus eros, vitae vehicula mi tincidunt vel. Aliquam quis magna dolor. Duis id erat a turpis dictum pellentesque ac quis mauris. Aenean sit amet pellentesque urna. Donec tincidunt leo in lorem dignissim, vel consequat sapien condimentum. Mauris in eleifend lectus. In euismod tristique tellus, a pharetra leo vestibulum et.

Nulla lectus libero, rhoncus vitae pellentesque nec, lobortis ac massa. Nam iaculis, nisl ornare suscipit ornare, ante leo tincidunt ex, ut maximus nunc lacus ut odio. Praesent eleifend maximus lacus, sed interdum ligula mattis a. Ut aliquet, ante eu pellentesque auctor, magna felis posuere metus, in faucibus lorem justo id sem. Duis vel tortor enim. Proin in est ut ante pulvinar fermentum. Aenean quis dictum nisi, a accumsan diam. Aenean facilisis auctor augue, quis aliquam purus dictum eu. Duis elementum venenatis aliquet. Donec ut nunc vel risus posuere commodo eget nec quam. Phasellus pellentesque rutrum odio, et efficitur turpis blandit eget. Ut non justo velit.

Nullam sem sem, gravida sit amet commodo at, pharetra ac risus. Aliquam erat volutpat. Vestibulum sit amet est auctor, rhoncus lectus in, sagittis leo. Nunc rutrum elit a ex bibendum mollis. Donec sagittis nisl mauris, eu cursus risus lobortis sit amet. Nam fringilla leo et nulla dictum dictum. Vivamus ac velit posuere, tempus urna quis, sagittis lorem. Mauris pellentesque aliquam risus, et laoreet eros congue id. Vivamus sit amet ex euismod, efficitur nibh vitae, mattis erat. Pellentesque rhoncus eros ut tellus porttitor, vel ornare justo imperdiet. Aliquam et ornare mauris. Sed lorem justo, molestie rhoncus nisl nec, ultricies tristique metus. In molestie est nunc, non facilisis tellus laoreet quis. Integer rhoncus, lacus vitae congue pretium, metus massa aliquet metus, vitae varius massa nisl vitae risus. Ut molestie sodales dignissim. Etiam varius scelerisque eros, eu tristique augue congue in.

Proin ullamcorper orci nulla, vulputate pretium magna cursus in. Donec maximus, augue id varius vehicula, diam est ultricies tortor, id semper mauris mauris in quam. Nullam sem elit, tempor eget aliquet sit amet, dapibus non velit. Etiam quis ante luctus, sagittis ex quis, tincidunt mi. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut mattis tincidunt turpis quis sollicitudin. Quisque sollicitudin ex ac velit gravida varius. Morbi ac accumsan nulla. Aliquam faucibus sapien ut mattis volutpat. Cras interdum neque enim, at consectetur ipsum pellentesque sed. Maecenas molestie gravida mollis. Pellentesque dictum convallis mi, non faucibus ligula. Curabitur consectetur turpis in sapien auctor tincidunt. Phasellus molestie faucibus diam, vel molestie justo pulvinar rutrum. Etiam vel nisi ullamcorper orci iaculis vestibulum eget eget dui. Vivamus tincidunt, mi in facilisis varius, ex lorem fermentum risus, vitae fringilla sapien nulla eget urna.

Quisque vulputate finibus mi, vel placerat ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec id mauris ut augue laoreet cursus. Pellentesque hendrerit ex nec nunc malesuada fringilla quis placerat risus. Vivamus euismod hendrerit ex eget laoreet. Aliquam in mauris ligula. Nunc quis scelerisque ante. Morbi condimentum nunc nec purus aliquet, ac sodales quam dictum. Morbi ipsum quam, aliquam sit amet porttitor et, ultrices nec eros.

Donec quis lectus rhoncus, rhoncus augue non, scelerisque lorem. In non porta sapien. Vestibulum at sodales elit. Pellentesque venenatis eu metus ut aliquam. Morbi pulvinar neque ut eros rhoncus facilisis. Praesent at convallis lacus. Mauris vehicula, nunc in interdum ultricies, quam ex convallis leo, eu tincidunt sem tellus id magna. Cras venenatis lobortis rutrum. Proin porta aliquet finibus. Nulla vehicula volutpat dolor, ut iaculis turpis cursus ut. Vivamus vehicula tempor auctor.

Donec porttitor maximus urna, quis tincidunt est vehicula at. Proin suscipit eu leo a ullamcorper. Donec et aliquam nunc. Sed rhoncus nisl pharetra, semper metus nec, laoreet turpis. Morbi interdum ligula ac egestas elementum. Nam mauris felis, vestibulum nec eros vel, lacinia accumsan nisl. Nam ut nisi odio. Ut lobortis, mauris posuere elementum convallis, ipsum nibh auctor neque, eu maximus nisi nibh vel neque. Ut euismod purus ac molestie elementum. Curabitur in nunc ipsum. Proin pharetra maximus ante quis aliquam.

Maecenas efficitur tristique ex, ut gravida arcu volutpat a. Nulla a tortor at neque dapibus gravida id quis augue. Pellentesque cursus felis faucibus posuere pellentesque. Nulla tempor venenatis imperdiet. Etiam eu tortor in turpis cursus rhoncus vitae nec odio. Curabitur vitae sapien turpis. Donec consequat lorem ex, a sollicitudin risus tristique eget. Nunc nec ultrices nulla, non laoreet nulla.

Quisque tincidunt tortor sit amet vulputate fringilla. Morbi et erat ex. Fusce gravida nisl ut purus condimentum feugiat. Nulla tempus sodales odio. Cras at.','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (4,'Prova con testo molto lungo','Risposta un po'' più corta','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (5,'Prova con testo molto lungo','Risposta un po'' più corta','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (6,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (8,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (9,'Prova con testo moltolung','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (10,'Prova con testo molto lung','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (11,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (12,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (13,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (14,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (15,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (16,'Prova con testo molto lungo','Risposta ancora più lunga','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (17,'prova','prova','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (18,'prova','prova','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (30,'lol','lol','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (31,'lol','lol','2023-09-02',0,0,NULL);
INSERT INTO "flashcards" VALUES (32,'Prova','Prova Ufficiale','2023-09-02',0,11,'C:/Users/Cristian Cinieri/Downloads/WIN_20230804_19_43_45_Pro.png');
INSERT INTO "flashcards" VALUES (33,'prova','prova','2023-09-02',0,0,'C:/Users/Cristian Cinieri/Downloads/WIN_20230804_19_43_45_Pro.png');
INSERT INTO "flashcards" VALUES (43,'Perso','Gelo','2023-09-02',0,11,NULL);
INSERT INTO "flashcards" VALUES (44,'Prova','prova','2023-09-10',0,11,'/home/cristian/Pictures/pT7r5aK6c.png');
INSERT INTO "sources" VALUES (0,'Casino',300,0,'C:/Users/Cristian Cinieri/Downloads/ticketdirect1226206334.pdf','2024-03-26','{''totalPages'': 10, ''totalDuration'': 100, ''MON'': {''isStudyDay'': False}, ''TUE'': {''isStudyDay'': True, ''areThereSessions'': True, ''amount'': 2, ''pages'': [10, 0], ''types'': [''Reading'', ''Testing''], ''durations'': [50, 50], ''totalPages'': 10, ''totalDuration'': 100}, ''WED'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''THU'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''FRI'': {''isStudyDay'': False}, ''SAT'': {''isStudyDay'': False}, ''SUN'': {''isStudyDay'': False}}',NULL,NULL,NULL,'2023-09-01','1','{}');
INSERT INTO "sources" VALUES (11,'Prova',300,0,'C:/Users/Cristian Cinieri/Downloads/goldoni dal 21-27.pdf','19-12-2023','{''totalPages'': 20, ''totalDuration'': 110, ''MON'': {''isStudyDay'': False}, ''TUE'': {''isStudyDay'': True, ''areThereSessions'': True, ''amount'': 2, ''pages'': [10, 10], ''types'': [''Reading'', ''Reading''], ''durations'': [50, 60], ''totalPages'': 20, ''totalDuration'': 110}, ''WED'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''THU'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''FRI'': {''isStudyDay'': False}, ''SAT'': {''isStudyDay'': False}, ''SUN'': {''isStudyDay'': False}}',NULL,NULL,NULL,'2023-09-01','0','{}');
INSERT INTO "sources" VALUES (12,'Prova',100,0,'','15-11-2023','{''totalPages'': 10, ''totalDuration'': 5, ''MON'': {''isStudyDay'': False}, ''TUE'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''WED'': {''isStudyDay'': True, ''areThereSessions'': True, ''amount'': 1, ''pages'': [10], ''types'': [''Reading''], ''durations'': [5], ''totalPages'': 10, ''totalDuration'': 5}, ''THU'': {''isStudyDay'': True, ''areThereSessions'': False, ''amount'': 0, ''pages'': [], ''types'': [], ''durations'': [], ''totalPages'': 0, ''totalDuration'': 0}, ''FRI'': {''isStudyDay'': False}, ''SAT'': {''isStudyDay'': False}, ''SUN'': {''isStudyDay'': False}}',NULL,NULL,NULL,'2023-09-10 11:15:54.012804',NULL,NULL);
COMMIT;
