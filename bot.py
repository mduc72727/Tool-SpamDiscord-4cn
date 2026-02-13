import os
import asyncio
import aiohttp
import logging
import random
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

CHANNEL_COLORS = [Fore.CYAN, Fore.YELLOW, Fore.GREEN, Fore.RED, Fore.MAGENTA]
MAX_CONCURRENT_REQUESTS = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("app.log"),
    logging.StreamHandler()
])

def print_header():
    header = f"""
{Fore.RED}{Style.BRIGHT}                                                                               
 
  ⠀⠸⣶⣦⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⢀⠀⢹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣷⣄⠨⣿⣿⣿⡌⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣷⣿⣿⣿⣿⣿⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣴⣾⣿⣮⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⠟⣹⣿⡿⢿⣿⣿⣬⣶⣶⡶⠦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣢⣙⣻⢿⣿⣿⣿⠎⢸⣿⠕⢹⣿⣿⡿⣛⣥⣀⣀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⡏⣿⡏⠿⢄⣜⣡⠞⠛⡽⣸⡿⣟⡋⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠾⠿⣿⠁⠀⡄⠀⠀⠰⠾⠿⠛⠓⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠠⢐⢉⢷⣀⠛⠠⠐⠐⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣠⣴⣶⣿⣧⣾⠡⠼⠎⢎⣋⡄⠆⠀⠱⡄⢉⠃⣦⡤⡀⠀⠀⠀⠀
⠀⠀⠐⠙⠻⢿⣿⣿⣿⣿⣿⣿⣄⡀⠀⢩⠀⢀⠠⠂⢀⡌⠀⣿⡇⠟⠀⠀⢄⠀
⠀⣴⣇⠀⡇⠀⠸⣿⣿⣿⣿⣽⣟⣲⡤⠀⣀⣠⣴⡾⠟⠀⠀⠟⠀⠀⠀⠀⡰⡀
⣼⣿⠋⢀⣇⢸⡄⢻⣟⠻⣿⣿⣿⣿⣿⣿⠿⡿⠟⢁⠀⠀⠀⠀⠀⢰⠀⣠⠀⠰
⢸⣿⡣⣜⣿⣼⣿⣄⠻⡄⡀⠉⠛⠿⠿⠛⣉⡤⠖⣡⣶⠁⠀⠀⠀⣾⣶⣿⠐⡀
⣾⡇⠈⠛⠛⠿⣿⣿⣦⠁⠘⢷⣶⣶⡶⠟⢋⣠⣾⡿⠃⠀⠀⠀⠰⠛⠉⠉⠀⠀   

  ____ Made by Nguyen Hoang Anh Duc              
 |  _ \ _   _  ___ ____  _ __  _   _ 
 | | | | | | |/ __|_  / | '_ \| | | |
 | |_| | |_| | (__ / / _| |_) | |_| |
 |____/ \__,_|\___/___(_) .__/ \__, |
                        |_|    |___/                                      
•Remakable: Phiên bản limited 🌟 🎨
    """
    print(header)

def print_author():
    author_info = f"""{Fore.CYAN}
 ↦  ↦  ↦  ↦  ↦  ↦  ↦  ↦  ↦  ↦  
↧ {Fore.RED}Copyright: Hoang Anh Duc   ↥
↧ {Fore.BLUE}Discord: sealedanw 🍪     ↥
↧ {Fore.GREEN}Instagram: not🏖️   ↥
↧ {Fore.MAGENTA}Zalo: not        ↥
 ↤  ↤  ↤  ↤  ↤  ↤  ↤  ↤  ↤  ↤  
    """
    print(author_info)
    
def print_instructions():
    instructions = f"""{Style.BRIGHT + Fore.WHITE}
⚙️  Dev Tool By Hoang Anh Duc 🖥️
⮕ Chức năng 1: Spam tin nhắn.
⮕ Chức năng 2: Nhây (tag hoặc để trống).
⮕ Chức năng 3: Nhây Fake Typing (giả soạn tin nhắn).
⮕ Chức năng 4: Réo tên ( có fake typing)
 Nhập số 1, 2, 3 or 4 để chọn chức năng.
 
 •••{Fore.YELLOW}Cách sử dụng tool•••
- Đối với chức năng 2,3,4. Bạn chọn y/n để tag hoặc không tag.
- Mỗi ID người tag cách nhau bằng dấu phẩy.
1. Nhập ID kênh (nhập done để kết thúc)
2. Nhập tên file chứa token cho từng kênh.
3. Chọn file chứa nội dung tin nhắn (cách ngôn=dấu phẩy).
4. Nhập delay token từng kênh.
    """
    print(instructions)

async def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return True
            else:
                logging.error(f"{Fore.RED}[UNAUTHORIZED] Token không hợp lệ: {token}")
                return False

async def load_tokens_from_file(token_file):
    if not os.path.exists(token_file):
        logging.error(f"File {token_file} không tồn tại.")
        return []
    
    with open(token_file, 'r', encoding='utf-8') as file:
        tokens = file.read().splitlines()
        
    if not tokens:
        logging.error(f"File {token_file} chứa token trống.")
    return tokens

async def handle_response(response, channel_id, message, token):
    if len(message.splitlines()) > 10:
        message_lines = message.splitlines()
        message = "\n".join(message_lines[:5] + message_lines[-5:])
    
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    message_words = message.split()
    message_preview = " ".join(message_words[:5]) + "..." + " ".join(message_words[-5:]) if len(message_words) > 10 else message
    
    try:
        if response.status == 200:
            logging.info(f"{Fore.GREEN}[DONE] Token {token_preview} đã gửi thành công tin nhắn: \"{message_preview}\" đến kênh {channel_id}.")
            return 0
        elif response.status == 429:
            retry_after = await response.json()
            retry_after_time = retry_after.get("retry_after", 1)
            logging.warning(f"{Fore.RED}[RATE LIMIT] Tạm dừng {retry_after_time} giây!")
            return retry_after_time
        elif response.status == 401:
            logging.error(f"{Fore.RED}[UNAUTHORIZED] Lỗi xác thực: Kiểm tra lại token cho kênh {channel_id}.")
            return 0
        elif response.status in [500, 502]:
            logging.warning(f"{Fore.RED}[SERVER ERROR] Lỗi máy chủ, thử lại sau!")
            return 5
        elif response.status == 408:
            logging.warning(f"{Fore.RED}[TIMEOUT] Yêu cầu timeout, thử lại!")
            return 5
        else:
            logging.error(f"{Fore.RED}[ERROR] Lỗi {response.status}: {await response.text()}")
            return 5
    except Exception as e:
        logging.error(f"{Fore.RED}[ERROR] Lỗi xử lý phản hồi: {e}")
        return 5

def get_valid_input(prompt, valid_func, error_message="Input không hợp lệ, vui lòng thử lại."):
    while True:
        user_input = input(prompt)
        if valid_func(user_input):
            return user_input
        else:
            print(error_message)

def is_valid_delay(input_str):
    try:
        delay = float(input_str)
        if delay <= 0:
            raise ValueError
        return True
    except ValueError:
        return False

def is_valid_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def is_valid_channel_id(input_str):
    return input_str.isdigit()


async def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}[ERROR] Tệp tin {file_path} không tồn tại.")
        return False
    return True

async def process_tokens(token_files):
    for token_file in token_files:
        if not await check_file_exists(token_file):
            continue
        tokens = await load_tokens_from_file(token_file)
        if not tokens:
            continue

async def handle_token_error(token, error):
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    logging.error(f"{Fore.RED}[TOKEN ERROR] Token {token_preview} gặp lỗi: {str(error)}. Bỏ qua token này và tiếp tục.")

async def spam_message(token, channel_id, message, delay, color, semaphore):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    if len(message) > 2000:
        logging.warning(f"{Fore.YELLOW}[WARNING] Tin nhắn dài hơn 2000 ký tự, sẽ bị cắt bớt.")
        message = message[:2000]
        logging.info(f"{Fore.YELLOW}[INFO] Tin nhắn đã bị cắt bớt xuống 2000 ký tự.")
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with semaphore:
                    async with session.post(url, json={"content": message}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        
                        if retry_after:
                            logging.info(f"{Fore.YELLOW}[INFO] Chờ {retry_after} giây trước khi thử lại.")
                            await asyncio.sleep(retry_after)
                        else:
                            await asyncio.sleep(delay + random.uniform(0.5, 1.5))
            except Exception as e:
                logging.error(f"{Fore.RED}[EXCEPTION] {str(e)}")
                await asyncio.sleep(1)
                continue

async def spam_message_nhay(token, channel_id, messages, delay, color, mention_user=False, user_ids=[], semaphore=None):
    if len(token) > 10:
        token_preview = token[:5] + "..." + token[-5:]
    else:
        token_preview = token

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    if user_ids:
        mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids])
    
    async with aiohttp.ClientSession() as session:
        while True:  # Vòng lặp vô tận
            for message in messages:
                try:
                    async with semaphore:
                        if mention_user:
                            message = f"{mention_string} {message}"
                        async with session.post(url, json={"content": message}, headers=headers) as response:
                            retry_after = await handle_response(response, channel_id, message, token)
                            if retry_after:
                                await asyncio.sleep(retry_after)
                            await asyncio.sleep(delay + random.uniform(0.5, 1.5))  # Delay ngẫu nhiên
                except Exception as e:
                    await handle_token_error(token, e)
                    break

async def fake_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    
    async with aiohttp.ClientSession() as session:
        while True:
            for message in messages:
                typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
                try:
                    async with session.post(typing_url, headers=headers):
                        logging.info(f"{Fore.CYAN}Đang soạn tin nhắn...")
                    for char in message:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        await asyncio.sleep(0.05)

                    async with semaphore:
                        message_to_send = f"{mention_string} {message}" if mention_user else message
                        while True:
                            async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                                retry_after = await handle_response(response, channel_id, message, token)
                                if retry_after:
                                    logging.info(f"{Fore.YELLOW}Đang chờ {retry_after} giây trước khi thử lại...")
                                    await asyncio.sleep(retry_after)
                                else:
                                    break
                    await asyncio.sleep(delay)
                except Exception as e:
                    await handle_token_error(token, e)
                    break

async def simulate_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore, name_to_call=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""
    
    async with aiohttp.ClientSession() as session:
        while True:
            for message in messages:
                typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
                try:
                    async with session.post(typing_url, headers=headers):
                        logging.info(f"{Fore.CYAN}Đang soạn tin nhắn...")
                    
                    if name_to_call:
                        message = message.replace("{name}", name_to_call)
                    
                    for char in message:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        await asyncio.sleep(0.05)

                    async with semaphore:
                        message_to_send = f"{mention_string} {message}" if mention_user else message
                        while True:
                            async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                                retry_after = await handle_response(response, channel_id, message, token)
                                if retry_after:
                                    logging.info(f"{Fore.YELLOW}Đang chờ {retry_after} giây trước khi thử lại...")
                                    await asyncio.sleep(retry_after)
                                else:
                                    break
                    await asyncio.sleep(delay)
                except Exception as e:
                    await handle_token_error(token, e)
                    break

async def main():
    print_header()
    print_author()
    print_instructions()

    choice = get_valid_input(f"{Style.BRIGHT + Fore.MAGENTA}Chọn chức năng (1: Spam, 2: Nhây, 3: Nhây Fake Typing, 4: Réo Tên): ", 
                             lambda x: x in ["1", "2", "3", "4"], "Lựa chọn không hợp lệ.")

    mention_user = False
    name_to_call = None
    if choice == "2" or choice == "3" or choice == "4":
        mention_user = input(f"{Style.BRIGHT + Fore.YELLOW}Có muốn tag người dùng không? (y/n): ").strip().lower() == 'y'
    
    if mention_user:
        user_ids_input = input(f"{Style.BRIGHT + Fore.YELLOW}Nhập ID người cần tag (cách nhau bởi dấu phẩy): ")
        user_ids = [user_id.strip() for user_id in user_ids_input.split(',')]
    else:
        user_ids = []

    if choice == "4":
        name_to_call = input(f"{Style.BRIGHT + Fore.YELLOW}Nhập tên cần réo: ").strip()

    channel_ids = []
    while True:
        channel_id_input = input(f"{Style.BRIGHT + Fore.MAGENTA}Nhập ID kênh (hoặc nhập 'done' để kết thúc): ")
        if channel_id_input.strip().lower() == "done":
            break
        elif is_valid_channel_id(channel_id_input):
            channel_ids.append(channel_id_input.strip())
        else:
            print(f"{Fore.RED}[ERROR] ID kênh không hợp lệ. Vui lòng thử lại.")

    tokens_map = {}
    for idx, channel_id in enumerate(channel_ids):
        color = CHANNEL_COLORS[idx % len(CHANNEL_COLORS)]
        token_file = input(f"{color}Tên file token cho kênh {channel_id}: ")

        tokens = await load_tokens_from_file(token_file)
        if not tokens:
            return

        for token in tokens:
            if not await validate_token(token):
                continue

        tokens_map[channel_id] = tokens

    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    if not txt_files:
        logging.error(f"Không tìm thấy file .txt nào trong thư mục.")
        return

    print(f"{Style.BRIGHT + Fore.CYAN}Các file .txt có sẵn:")
    for idx, file_name in enumerate(txt_files):
        print(f"{Style.BRIGHT + Fore.GREEN}{idx + 1}. {file_name}")

    try:
        file_indexes = input(f"{Style.BRIGHT + Fore.YELLOW}Chọn file chứa tin nhắn (nhập số thứ tự, cách nhau bởi dấu phẩy): ")
        file_indexes = [int(i) - 1 for i in file_indexes.split(',')]
        if any(index < 0 or index >= len(txt_files) for index in file_indexes):
            logging.error(f"Chọn file không hợp lệ.")
            return
    except ValueError:
        logging.error(f"Vui lòng nhập số hợp lệ.")
        return

    files_content = []
    for file_index in file_indexes:
        file_path = txt_files[file_index]
        with open(file_path, 'r', encoding='utf-8') as file:
            files_content.append(file.read())

    tasks = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    for idx, (channel_id, tokens) in enumerate(tokens_map.items()):
        color = CHANNEL_COLORS[idx % len(CHANNEL_COLORS)]
        for i, token in enumerate(tokens):
            try:
                delay = float(input(f"{Style.BRIGHT + color}Nhập delay cho token thứ {i + 1} (kênh {channel_id}): "))

                if choice == "1":
                    tasks.append(spam_message(token, channel_id, files_content[i % len(files_content)], delay, color, semaphore))
                elif choice == "2":
                    messages = files_content[i % len(files_content)].splitlines()
                    tasks.append(spam_message_nhay(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore))
                elif choice == "3":
                    messages = files_content[i % len(files_content)].splitlines()
                    tasks.append(simulate_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore))
                elif choice == "4":
                    messages = files_content[i % len(files_content)].splitlines()
                    tasks.append(simulate_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore, name_to_call))

            except ValueError:
                logging.error(f"Delay phải là số hợp lệ.")
                return

    logging.info(f"\n{Style.BRIGHT + Fore.MAGENTA}RUN BY BRIAN⚡\n")
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())
