import main
import customtkinter as ctk


def om(ch):
    if ch == 'Светлый фон':
        ctk.set_appearance_mode("light")
    elif ch == 'Тёмный фон':
        ctk.set_appearance_mode("dark")


def cmb(ch):
    entry_input.delete(0, "end")
    if ch in ["9. Получить список всех авторов", "10. Получить список всех книг в алфавитном порядке"]:
        entry_input.configure(state="disabled")
    else:
        entry_input.configure(state="normal", placeholder_text='')
    if ch in ['5. Найти книги, написанные в указанный период времени',
              '6. Найти книги со средней стоимостью в указанном диапазоне', '7. Найти книги по количеству страниц']:
        entry_input_add.grid(row=4, column=2, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")
        entry_input.configure(placeholder_text='От')
    else:
        entry_input_add.grid_forget()


def handle_pressing_btn_result():
    input_data = entry_input.get()
    input_data_add = entry_input_add.get()
    output_data = set()
    if cmbbox_operations.get() == "1. Получить все книги указанного автора":
        output_data = main.search(input_data, 'Автор')
    elif cmbbox_operations.get() == "2. Найти книги по стране оригинала":
        output_data = main.search(input_data, "Страна оригинала")
    elif cmbbox_operations.get() == "3. Найти книги по жанру":
        output_data = main.search(input_data, 'Жанр')
    elif cmbbox_operations.get() == "4. Найти книги с рейтингом Litres, выше указанного":
        output_data = main.search(input_data, 'Рейтинг Litres')
    elif cmbbox_operations.get() == "5. Найти книги, написанные в указанный период времени":
        output_data = main.span(int(input_data), int(input_data_add), 'Год написания')
    elif cmbbox_operations.get() == "6. Найти книги со средней стоимостью в указанном диапазоне":
        output_data = main.span(int(input_data), int(input_data_add), 'Средняя стоимость (в рублях)')
    elif cmbbox_operations.get() == "7. Найти книги по количеству страниц":
        output_data = main.span(int(input_data), int(input_data_add), 'Объём книги (в страницах)')
    elif cmbbox_operations.get() == "8. Получить информацию о книге по названию":
        output_data.add(main.book_info(input_data))
    elif cmbbox_operations.get() == "9. Получить список всех авторов":
        output_data = main.roster('Автор')
    elif cmbbox_operations.get() == "10. Получить список всех книг в алфавитном порядке":
        output_data = main.roster()
    entry_output.configure(state="normal")
    entry_output.delete("0.0", "end")
    if output_data:
        for x in output_data:
            entry_output.insert(0.0, x + '\n')
    else:
        entry_output.insert(0.0, 'Книги не найдены.')
    entry_output.configure(state="disabled")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Библиотека")
root.geometry("1000x500")

lbl_start_message = ctk.CTkLabel(master=root)
lbl_start_message.configure(text="Выберите условия поиска книг:",
                            font=ctk.CTkFont(family='Arial', size=15, weight='bold', slant='italic'))

operations = ["1. Получить все книги указанного автора", "2. Найти книги по стране оригинала",
              '3. Найти книги по жанру', '4. Найти книги с рейтингом Litres, выше указанного',
              '5. Найти книги, написанные в указанный период времени',
              '6. Найти книги со средней стоимостью в указанном диапазоне', '7. Найти книги по количеству страниц',
              '8. Получить информацию о книге по названию', '9. Получить список всех авторов',
              '10. Получить список всех книг в алфавитном порядке']
cmbbox_operations = ctk.CTkComboBox(master=root)
cmbbox_operations.configure(justify="center", values=operations, state="readonly",
                            font=ctk.CTkFont(family='Arial', size=15), command=cmb)
cmbbox_operations.set("1. Получить все книги указанного автора")

lbl_input, lbl_output = ctk.CTkLabel(master=root), ctk.CTkLabel(master=root)
lbl_input.configure(text="Введите данные:", font=ctk.CTkFont(family='Arial', size=20, weight='bold'))
lbl_output.configure(text="Результат поиска:", font=ctk.CTkFont(family='Arial', size=20, weight='bold'))

entry_input = ctk.CTkEntry(master=root)
entry_input.configure(justify="center", font=ctk.CTkFont(family='Arial', size=15))

entry_input_add = ctk.CTkEntry(master=root)
entry_input_add.configure(justify="center", font=ctk.CTkFont(family='Arial', size=15), placeholder_text='До')

entry_output = ctk.CTkTextbox(master=root)
entry_output.configure(state="disabled", wrap='word', font=ctk.CTkFont(family='Arial', size=15))

btn_result = ctk.CTkButton(master=root)
btn_result.configure(text="Найти", command=handle_pressing_btn_result,
                     font=ctk.CTkFont(family='Arial', size=15, weight='bold'))

menu = ctk.CTkOptionMenu(master=root)
menu.configure(anchor='center', values=['Светлый фон', 'Тёмный фон'],
               font=ctk.CTkFont(family='Arial', size=15, weight='bold', slant='italic'), command=om)
menu.set('Выберите тему фона')
menu.grid(row=0, column=3, padx=20, pady=20, sticky="ew")

rows, columns = 7, 7
for i in range(rows):
    root.rowconfigure(index=i, weight=1)
for i in range(columns):
    root.columnconfigure(index=i, weight=1)

lbl_start_message.grid(row=1, column=3, ipadx=4, ipady=4, padx=4, pady=4, sticky="ew")
cmbbox_operations.grid(row=2, column=3, sticky="ew")
lbl_input.grid(row=3, column=1, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")
lbl_output.grid(row=3, column=4, columnspan=2, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")
entry_input.grid(row=4, column=1, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")
entry_output.grid(row=4, column=4, columnspan=2, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")
btn_result.grid(row=5, column=3, ipadx=4, ipady=4, padx=6, pady=6, sticky="nsew")

root.mainloop()
