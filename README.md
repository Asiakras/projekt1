Program do Transformacji Geodezyjnych - projekt na zajecia Informatyka Geodezyjna sem. 4
Program służy do przeprowadzania transformacji geodezyjnych pomiędzy różnymi układami współrzędnych. Oferuje następujące funkcjonalności:
- Transformacja współrzędnych XYZ na współrzędne geodezyjne (BLH) - funkcja xyz2plh.
- Transformacja współrzędnych geodezyjnych (BLH) na współrzędne XYZ - funkcja plh2xyz.
- Transformacja współrzędnych geodezyjnych (BL) na współrzędne PL-2000 - funkcja pl2000.
- Transformacja współrzędnych XYZ na współrzędne NEU - funkcja xyz2neu.
- Transformacja współrzędnych geodezyjnych (BL) na współrzędne PL-1992 - funkcja pl1992.

Wymagania systemowe:
Aby program działał poprawnie, wymagane są:
- Python w wersji 3.x.
- Biblioteka NumPy.
System operacyjny:
- Program był robiony i testowany na systemie Windows 10, więc ten system i jego wersja jest zalecana.
 Użycie programu:
- Program można uruchomić z wiersza poleceń, podając odpowiednie argumenty. Poniżej znajdują się przykładowe wywołania programu wraz z opisem:

Transformacja XYZ na BLH:
 python program.py input_xyz.txt header_lines liczba model xyz2plh
 input_xyz.txt: plik zawierający współrzędne XYZ.
 header_lines: fraza implementujaca ustawienie liczby linijek nagłówka.
 liczba: liczba linii nagłówka, które program musi zignorować.
 model: model elipsoidy (WGS84, GRS80, mars).
 xyz2plh: flaga informująca o wybraniu funkcji transformacji z XYZ na BLH.
 Wyniki zostaną zapisane do pliku result_xyz2plh.txt.

Transformacja BLH na XYZ:
 python program.py input_blh.txt header_lines model plh2xyz
 input_blh.txt: plik zawierający współrzędne BLH.
 header_lines: fraza implementujaca ustawienie liczby linijek nagłówka.
 liczba: liczba linii nagłówka, które program musi zignorować.
 model: model elipsoidy (WGS84, GRS80, mars).
 plh2xyz: flaga informująca o wybraniu funkcji transformacji z BLH na XYZ.
 Wyniki zostaną zapisane do pliku result_plh2xyz.txt.

Transformacja BLH na PL-2000:
 python program.py input_blh.txt header_lines liczba model pl2000
 input_blh.txt: plik zawierający współrzędne BLH.
 header_lines: fraza implementujaca ustawienie liczby linijek nagłówka.
 liczba: liczba linii nagłówka, które program musi zignorować.
 model: model elipsoidy (WGS84, GRS80, mars).
 pl2000: flaga informująca o wybraniu funkcji transformacji z BLH na PL-2000.
 Wyniki zostaną zapisane do pliku result_pl2000.txt.

Transformacja XYZ na NEU:
 python program.py input_xyz.txt header_lines liczba wspX0 wspY0 wspZ0 xyz2neu
 input_xyz.txt: plik zawierający współrzędne XYZ.
 header_lines: fraza implementujaca ustawienie liczby linijek nagłówka.
 liczba: liczba linii nagłówka, które program musi zignorować.
 wspX0 wspY0 wspZ0: początkowe współrzędne XYZ.
 xyz2neu: flaga informująca o wybraniu funkcji transformacji z XYZ na NEU.
 Wyniki zostaną zapisane do pliku result_xyz2neu.txt.

Transformacja BLH na PL-1992:
 python program.py input_blh.txt header_lines liczba wgs84 pl1992
 input_blh.txt: plik zawierający współrzędne BLH.
 header_lines: fraza implementujaca ustawienie liczby linijek nagłówka.
 liczba: liczba linii nagłówka, które program musi zignorować.
 model: model elipsoidy (WGS84, GRS80, mars).
 pl1992: flaga informująca o wybraniu funkcji transformacji z BLH na PL-1992.
 Wyniki zostaną zapisane do pliku result_pl1992.txt.

Znane problemy:
- Obsługiwane są tylko 3 modele elipsoid więc wpisujac jakikolwiek inny model wyskoczy powiadomienie o tym że podany model nie jest obsługiwany oraz wyskakuje też powiadomienie 
"Traceback (most recent call last):
  File "C:\Users\kubak\Desktop\projinf\inf_geo_proj1.py", line 247, in <module>
    geo = Transformacje(model=ellipsoid_model)
                              ^^^^^^^^^^^^^^^
NameError: name 'ellipsoid_model' is not defined" mimo tego program wstzrymuje działanie i nie podaje wyników.
- Możliwe błędy w przypadku danych wejściowych o nietypowej strukturze lub wartościach.
- Program nie obsługuje automatycznego wykrywania liczby linii nagłówkowych w pliku, użytkownik musi podać dokladną i pełną wartość
