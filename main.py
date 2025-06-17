import datetime
import psutil  # для работы с дисками

def get_disk_usage():
    # Получает информацию о диске C:
    try:
        disk = psutil.disk_usage('C:')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    except Exception as e:
        return {'error': str(e)}

def write_to_log(disk_info):
    # Записывает информацию в лог-файл
    log_file = 'storage.log'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(log_file, 'a', encoding='utf-8') as f:
        if 'error' in disk_info:
            f.write(f"{timestamp} - Ошибка: {disk_info['error']}\n")
        else:
            # Конвертируем байты в гигабайты для удобства чтения
            total_gb = disk_info['total'] / (1024 ** 3)
            used_gb = disk_info['used'] / (1024 ** 3)
            free_gb = disk_info['free'] / (1024 ** 3)

            f.write(
                f"{timestamp} - Диск C: | Всего: {total_gb:.2f} GB | "
                f"Использовано: {used_gb:.2f} GB ({disk_info['percent']}%) | "
                f"Свободно: {free_gb:.2f} GB\n"
            )

def main():
    disk_info = get_disk_usage()
    print('Была проведена диагностика. Смотрите файл "storage.log"')
    write_to_log(disk_info)
    input()

if __name__ == "__main__":
    main()