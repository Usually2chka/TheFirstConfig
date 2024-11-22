- Класс Emulator: Основной класс, который загружает конфигурацию и управляет виртуальной файловой системой.
- Методы: 
  - load_config: Загружает конфигурацию из XML-файла.
  - load_virtual_fs: Извлекает содержимое tar-архива.
  - ls, cd, exit, chmod, date, tail: Реализация команд, которые могут быть вызваны пользователем.
- Основной цикл: Запрашивает команды у пользователя и выполняет соответствующие методы.

1. **setUpClass и tearDownClass:**
Эти методы создают тестовые данные и очищают их после завершения всех тестов. Мы создаем временный tar-архив с двумя файлами для тестирования.
  
2. **test_ls:**
Проверяет, что команда `ls` возвращает правильные файлы в текущем каталоге.

3. **test_cd_valid и test_cd_invalid:**
Проверяют поведение команды `cd` при переходе в существующий и несуществующий каталог.

4. **test_exit:**
Проверяет корректную работу команды `exit`.

5. **test_chmod:**
Проверяет, что команда `chmod` возвращает правильное сообщение.

6. **test_date:**
Проверяет, что команда `date` возвращает текущую дату в нужном формате.

7. **test_tail_valid:**
Проверяет правильность работы команды `tail` для существующего файла.

8. **test_tail_invalid:**
Проверяет поведение команды `tail` при попытке получить содержимое несуществующего файла.

9. **test_tail_no_lines:**
Проверяет, что команда `tail` возвращает пустую строку, если запрашивается 0 строк.
