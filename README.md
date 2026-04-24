# Tickets Bot for Support Team

Бот для отслеживания новых тикетов в YouTrack

## Содержание
- [Требования](#требования)
- [Установка](#установка)
- [Настройка локальных переменных](#настройка-локальных-переменных)
- [Сборка и деплой](#сборка-и-деплой)
- [Опционально](#опционально-(для-NtechLab))

## Требования

Для запуска и сборки требуется установленный docker и docker compose **второй** версии

1. [Установка Docker](https://docs.docker.com/engine/install/ubuntu/)

2. Установка Docker Compose V2
```sh
sudo apt update && sudo apt install docker-compose-v2
```

## Установка

1. Клонировать репозиторий
```sh
git clone https://github.com/Shiretomi/jetbrains_ticket_tracker && cd jetbrains_ticket_tracker
```

## Настройка локальных переменных

1. Переименовать .env.example в .env и заменить переменные внутри файла на нужные
```sh
mv .env.example .env && nano .env
```

## Сборка и деплой

1. Запустить проект со сборкой
```sh
docker compose up -d --build
```

### На этом всё!

Для последующих перезапусков сборка не требуется, если обновлений в репозитории не было
```sh
docker compose up -d
```

## Опционально (для NtechLab)
### Для включение обновления FFMulti через ansible

1. Перейти в папку ./ansible и переименовать hosts.ini.example и update.yml.example в аналогичные hosts.ini и update.yml
```sh
cd ./ansible && mv hosts.ini.example hosts.ini && mv update.yml.example update.yml
```
2. Создать сервисный ssh ключ для контейнера (при создании указать имя id_rsa_service)
```sh
ssh-keygen -t rsa
```

3. Перенести полученный id_rsa_service в папку ./ansible
```sh
mv ~/.ssh/id_rsa_service ./
```

4. Закинуть публичный ключ на целевую машину

5. В hosts.ini указать хосты, которые можно обновить
```
hostname - Хостнейм машины для update.yml 
ansible_host - IP Адрес хоста  
ansible_user - Пользователь, под котором будет происходить обновление
ansible_ssh_private_key_file - Путь до ssh private ключа в контейнере, просто положите ключ в директорию ./ansible 
ansible_ssh_extra_args - Параметр, чтобы ssh не ругался на фингерпринт, советую оставить '-o StrictHostKeyChecking=no'
```

6. В update.yml обновить переменные
```
hosts - Хостнейм из hosts.ini
ansible_python_interpreter - Интерпритатор питона, убедиться, что на целевой машине указанная версия питона
installer_url - Ссылка на репозиторий с мульти (указывать в формате "http://url/")
destination - Директорию с версией мульти (указывать в формате "multi-x.x.x/")
tmp_folder - Куда будет происходить загрузка и распаковка установщика на целевой машине
container_name - Имя контейнера UI на целевой машине  
```

### ВСЁ. После этого, команда /update_supdemo в боте заработает без ошибок 
