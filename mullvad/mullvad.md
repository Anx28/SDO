Ниже проброс на порты через мулвад (если используется как клиент)
```
table inet excludeTraffic {
  chain allowIncoming {
    type filter hook input priority -100; policy accept;
    tcp dport 22 ct mark set 0x00000f41 meta mark set 0x6d6f6c65;
  }

  chain allowOutgoing {
    type route hook output priority -100; policy accept;
    tcp sport 22 ct mark set 0x00000f41 meta mark set 0x6d6f6c65;
  }
  chain allowIncoming {
    type filter hook input priority -100; policy accept;
    tcp dport 3389 ct mark set 0x00000f41 meta mark set 0x6d6f6c65;
  }

  chain allowOutgoing {
    type route hook output priority -100; policy accept;
    tcp sport 3389 ct mark set 0x00000f41 meta mark set 0x6d6f6c65;
  }
}
```

---
Для виндовс
Mullvad - включить сплит туннель. 
  ДОбавить два процесса C:\Windows\System32\Svchost.exe  и mstsc.exe (он же рдп).
  

Скрипт рандомной смены локации. (выбирает из доступных, пишет об этом). Частоту смен настраивать через крон.
```
  #!/bin/bash

# Получаем список доступных стран и городов в формате country-city
locations=$( mullvad relay list | sed 's/^[ \t]*//' | sed '/^[A-Z]/d' | sed '/^$/d' |awk '{print $1}')

# Выбираем случайную локацию
random_location=$(echo "$locations" | shuf -n 1)

# Проверяем, подключен ли Mullvad VPN
mullvad_status=$(mullvad status | grep -o "Connected" || echo "Disconnected")

if [[ "$mullvad_status" == "Connected" ]]; then
    echo "Отключение от текущего сервера Mullvad..."
    mullvad disconnect
    sleep 2  # Небольшая пауза для безопасного отключения
fi

# Устанавливаем случайный сервер
echo "Подключение к новому серверу Mullvad в локации: $random_location"
mullvad relay set location "$random_location"

# Подключаемся снова
mullvad connect

sleep 2
# Проверяем результат
if mullvad status | grep -q  "Connected"; then
    echo "Подключено к новой локации: $random_location"
else
    echo "Ошибка подключения к новой локации."
fi
  ```
