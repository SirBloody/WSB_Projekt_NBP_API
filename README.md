# WSB_Projekt_NBP_API

Projekt składa się z 3 modułów oraz 2 plików źródłowych ze znakami walut oraz ich nazwami

- app.py
- import_from_file_to_list.py
- prevents.py

- currencies.txt
- currency_name.txt

Do działania aplikacji niezbędne są:

- tkinter
- httpx


Moduł app.py służy do uruchomienia aplikacji, iniciuje on za pomocą biblioteki Tkinter interfejs okienkowy.

Rozmiaru okienka nie można zmieniać dzięki flagą False w root.resizable
Okienko wyświetla się zawsze na środku ekranu dzięki zaczytaniu parametrów ekranu za pomocą root.winfo

Szerokość okienka jest zawsze 1/4 szerokości wyświetlacza, a wyskokość ustawiona na stałe na 700px

Dodana została duża czcionka large_font za pomocą modułu font.py z biblioteki tkinter

Definiowana jest dzisiejsza data today za pomocą modułu date z biblioteki datetime, służy ona do zapobiegania wybrania daty z przyszłości podczas przeliczania kursów

Później za pomocą modułu import_from_file_to_list.py w którym znajdują się funkcje do przetworzenia plików tekstowych na listy, importowane są waluty oraz ich nazwy.
-lista currencies
-lista name

Definiowana jest wartość wigedtu ComboBox jako string
combo_val = tk.StringVar()

Ustawiana jest domyślna waluta
combo_val.set(currencies[])

Funkcja dynamic_label(event) służy do powiązania wybranej wartości z wigedtu Combobox z wigetem label3, aby ten wyświetlał nazwę wybranej waluty (indeks danej waluty na liscie currencies odpowiada indeksowi na liście name np. currencies[9] = EUR name[9]= Euro)

Główna funkcja to funkcja get_rates(selected_date, currency, amount, attempt=0)
Użyty został try except, ponieważ użytkownik może wybrać datę, w której odczyt kursu nie występuje, w tym przypadku program zwraca wyjątek z błędem, który musi zostać ujęty.
Na początku sprawdzana jest wartość amount, gdyż użytkownik może jej nie wypełnić, w tym przypadku wartość amount jest ustawiana na wartość domyślną 1
Następnie definiowane jest url do api nbp ze zmiennymi currency oraz selected_date.
Zmienna resp używa httpx.get(url), dzięki temu możemy zaciągnąć dane oraz przypisać je do znmiennej data.
Użyta zostaje funkcja resp.rise_for_status(), która zwraca HTTPError jeśli on wystąpi.
Zmienna rate jest odpowiednikiem kursu średniego wyciągniętego z resp.json.
Następnie czyszczony jest output_text z wigetu Text, gdyby użytkownik chciał wybrać inną walutę, okienko zostanie wyczyszczone z poprzeniego wyboru.
  Następnie wporwadzane są dane do wigetu output_text takie jak:
    - Kurs wymiany zadanej waluty do złotówki (1 do 1)
    - Data z której kurs został zaczytany
    - Przeliczenie podanej ilość walut obcych na złotówki (np. 100 EUR = xxx PLN)

  Wychwytywane są dwa wyjątki:
  
  -HTTPStatusError w przypadku gdyby użytkownik trafił na datę, w której nie ma odczytu kursu
    W tym przypadku została użyta funkcja warunkowa if else.
    Została użyta zmienna attempt w celu zapobiegnięciu pętli rekurencyjnej (np. jeśli użytkownik wybierze datę z poprzedniego wieku, program zapętliłby się, gdyż sprawdza dni poprzedzające wybraną datę)
    Definiowana jest zmienna prev_date za pomocą modułu datetime oraz timedelta
    Ponownie wywoływana jest funkcja get_rates lecz selected_date jest zastępowane prev_date oraz do zmiennej attempt jest dodwane 1)
    Pętla zakończy się jęsli data zostanie znaleziona w przeciwnym wypadku zostanie zastosowana instrukcja else czyli komunikat iż nie udało znaleźć się kursów w zadanej dacie ani pobliskich datach

  -RequestError w przypadku gdyby użytkownik nie posiadał połączenia z internetem, wyjątek zwróci komunikat iż żądanie się nie powiodło oraz proszony jest o sprawdzenie połąćzenia internetowego.



Tworozna jest zmienna input_var, która ma przechowywać wpisaną wartość

Tworzona jest zmienna validate, która ma przypisaną funkcję sprawdzającą z modułu prevents.py, która ma wymuszać na użytkowniku wprowadzaniu tylko i wyłącznie int oraz float w wigecie Entry

Następnie są definiowane wigety:

  - cal - wiget Calendar : Dodaje do okienka graficzny kalendarz, z którego użytkownik wybiera datę z której chce sprawdzić kurs, użyte zostały takie parametry jak selectmode date_pattern oraz maxdate
  - label1 label2 label3 : wiget Label: Dodaje do okienka etykietę z napisem, oprócz parametru text= dodany jest również parametr font= który pozwala nam na zastosowanie wcześniej zdefiniowanej czcionki, label3 jest zawarty w funkcji dynamic_label za pomocą label3.config(text=)
  - entry - wiget Entry : Dodaje do okienka pole do wprowadzenia danych użytkownika, wykorzystywana jest tutaj zmienna input_var w parametrze textvariable, dodatkowo zastosowany został parametr validate który ma sprawdzać kliawisze oraz validatecommand do którego przypisujemy wcześniej zdefiniowane validate
    oraz parametr %P który reprezentuje nową wartość wpisu po bieżacej edycji
  - combo_box - wiget Combobox : Dodaje do okienka rozwijaną listę, wykorzystywana jest zmienna combo_val w parametrze textvariable, parametr values przedstawia zawartość listy currencies, parametr state='readonly' został użyty aby użytkownik nie mógł edytować zawartości.
  - output_text - wiget Text : Dodaje okienko w którym wyświetlane są kursy walut oraz data
  - get_rates_button - wiget Button : Dodaje przycisk, który wywołuje funkcje zdefiniowaną w parametrze command, została funkcja lambda, aby przekazać niezbędne parmametry do funkcji get_rates

  Do każdego wigetu został zastosowany grid, dzięki któremu można ustawić odpowiednio wigetu za pomocą parametrów row= column= padx= pady=
  
Przypisana zostaje funkcja z modułu prevents do wigetu output_text, która ma na celu zapobiegnięcie usuwania tekstu z okienka output
Przypisana zostaje funkcja dynamic_label do wigetu combo_box, która ma za zadanie zmianę label3 po zmianie wyboru z listy wigetu combo_box
  
  
