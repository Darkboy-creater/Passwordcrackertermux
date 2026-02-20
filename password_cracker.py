#!/data/data/com.termux/files/usr/bin/python3
"""
PASSWORD CRACKER - Educational Tool for Termux
ONLY for testing YOUR OWN passwords!
"""

import os
import sys
import time
import json
import hashlib
import itertools
import string
import threading
from queue import Queue
from datetime import datetime
from colorama import init, Fore, Style, Back

init(autoreset=True)

# ==================== CONFIGURATION ====================
class Config:
    VERSION = "2.0"
    
    BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║             PASSWORD CRACKER v{VERSION} - Termux               ║
║           owner_maxod_ethical hacker        ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    
    DISCLAIMER = f"""
{Fore.RED}══════════════════════════════════════════════════════════════
⚠️  IMPORTANT LEGAL NOTICE ⚠️
══════════════════════════════════════════════════════════════
This tool is for EDUCATIONAL PURPOSES ONLY.
Use ONLY to test passwords you OWN or have PERMISSION to test.
Unauthorized password cracking is ILLEGAL and punishable by law.
You are responsible for your own actions.{Style.RESET_ALL}
    """
    
    # Password patterns for generation
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "1234", "qwerty", "12345",
        "dragon", "football", "baseball", "welcome", "abc123",
        "111111", "123123", "admin", "letmein", "monkey", "login",
        "passw0rd", "master", "hello", "freedom", "whatever",
        "qazwsx", "trustno1", "654321", "jordan23", "harley",
        "password1", "1234567", "sunshine", "iloveyou", "starwars",
        "computer", "superman", "princess", "michelle", "1111",
        "131313", "1234567890", "hello123", "charlie", "aa123456"
    ]

# ==================== PASSWORD GENERATOR ====================
class PasswordGenerator:
    @staticmethod
    def generate_from_info(name="", birth_date="", keywords=[]):
        """Generate passwords from personal information"""
        passwords = set()
        
        # Name-based passwords
        if name:
            name_lower = name.lower()
            name_parts = name_lower.split()
            
            if name_parts:
                first = name_parts[0]
                last = name_parts[-1] if len(name_parts) > 1 else ""
                
                # Basic combinations
                passwords.update([
                    first,
                    last,
                    first + last,
                    first + "." + last,
                    first + "_" + last,
                    first[0] + last,
                    first + last[0],
                    first.capitalize() + last.capitalize(),
                    first + "123",
                    first + "1234",
                    first + "12345",
                    first + "!",
                    first + "@",
                    first + "#",
                ])
        
        # Birth date passwords
        if birth_date:
            try:
                # Try different date formats
                for fmt in ["%d-%m-%Y", "%d/%m/%Y", "%d%m%Y", "%Y%m%d"]:
                    try:
                        dt = datetime.strptime(birth_date, fmt)
                        day = str(dt.day).zfill(2)
                        month = str(dt.month).zfill(2)
                        year = str(dt.year)
                        year_short = year[2:]
                        
                        passwords.update([
                            day + month + year,
                            day + month + year_short,
                            year + month + day,
                            year_short + month + day,
                            month + day + year,
                            day + month,
                            month + day,
                        ])
                    except:
                        continue
            except:
                pass
        
        # Keyword-based passwords
        for keyword in keywords:
            if keyword:
                passwords.add(keyword)
                for num in range(100):
                    passwords.add(keyword + str(num))
                    passwords.add(keyword + str(num).zfill(2))
                for symbol in ["!", "@", "#", "$", "%", "&", "*"]:
                    passwords.add(keyword + symbol)
        
        return list(passwords)
    
    @staticmethod
    def generate_bruteforce(min_len=1, max_len=4, charset=string.ascii_lowercase):
        """Generate brute force combinations"""
        passwords = []
        for length in range(min_len, max_len + 1):
            for combo in itertools.product(charset, repeat=length):
                passwords.append(''.join(combo))
        return passwords
    
    @staticmethod
    def load_wordlist(filename):
        """Load passwords from wordlist file"""
        if not os.path.exists(filename):
            return []
        
        passwords = []
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        passwords.append(line)
            return list(set(passwords))  # Remove duplicates
        except:
            return []

# ==================== HASH CRACKER ====================
class HashCracker:
    def __init__(self, hash_type="md5"):
        self.hash_type = hash_type.lower()
        self.hash_func = getattr(hashlib, self.hash_type, None)
        if not self.hash_func:
            raise ValueError(f"Unsupported hash type: {hash_type}")
    
    def crack(self, target_hash, passwords):
        """Try to crack a hash"""
        print(f"{Fore.CYAN}[*] Cracking {self.hash_type.upper()} hash: {target_hash[:16]}...{Style.RESET_ALL}")
        
        start_time = time.time()
        total = len(passwords)
        found = None
        
        for i, password in enumerate(passwords, 1):
            # Calculate hash
            try:
                hashed = self.hash_func(password.encode()).hexdigest()
            except:
                continue
            
            # Check if it matches
            if hashed == target_hash.lower():
                found = password
                break
            
            # Display progress every 100 attempts
            if i % 100 == 0 or i == total:
                elapsed = time.time() - start_time
                percent = (i / total) * 100
                speed = i / elapsed if elapsed > 0 else 0
                
                bar_length = 30
                filled = int(bar_length * percent // 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"\r{Fore.YELLOW}[{bar}] {percent:.1f}% | {i}/{total} | {speed:.1f}/sec{Style.RESET_ALL}", end='')
        
        print()  # New line after progress
        
        return found

# ==================== PASSWORD STRENGTH TESTER ====================
class PasswordStrengthTester:
    @staticmethod
    def test_strength(password):
        """Test password strength"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        else:
            score += 1
            feedback.append("Too short (min 8 chars recommended)")
        
        # Character variety
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if has_lower:
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if has_upper:
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Add numbers")
        
        if has_special:
            score += 2
        else:
            feedback.append("Add special characters (!@#$% etc.)")
        
        # Check against common passwords
        if password.lower() in Config.COMMON_PASSWORDS:
            score = 1
            feedback.append("Very common password")
        
        # Determine strength level
        if score >= 8:
            strength = "Strong"
            color = Fore.GREEN
        elif score >= 5:
            strength = "Moderate"
            color = Fore.YELLOW
        else:
            strength = "Weak"
            color = Fore.RED
        
        return {
            "score": score,
            "strength": strength,
            "color": color,
            "feedback": feedback,
            "length": len(password),
            "has_lower": has_lower,
            "has_upper": has_upper,
            "has_digit": has_digit,
            "has_special": has_special
        }

# ==================== MAIN APPLICATION ====================
class PasswordCrackerApp:
    def __init__(self):
        self.mode = ""
        self.target = ""
        self.passwords = []
    
    def display_menu(self):
        """Display main menu"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(Config.BANNER)
        print(Config.DISCLAIMER)
        
        print(f"\n{Fore.CYAN}═══ MAIN MENU ═══{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Hash Cracking (MD5, SHA1, SHA256)")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Password Strength Tester")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Dictionary Attack Simulation")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Brute Force Simulation (Simple)")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Personal Information Attack")
        print(f"{Fore.GREEN}[0]{Style.RESET_ALL} Exit")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}[?] Select option (0-5): {Style.RESET_ALL}").strip()
            if choice in ['0', '1', '2', '3', '4', '5']:
                return choice
            print(f"{Fore.RED}[-] Invalid choice{Style.RESET_ALL}")
    
    def hash_cracking_mode(self):
        """Hash cracking mode"""
        print(f"\n{Fore.CYAN}═══ HASH CRACKING ═══{Style.RESET_ALL}")
        
        # Hash type selection
        hash_types = ['md5', 'sha1', 'sha256', 'sha512']
        print(f"\n{Fore.YELLOW}Available hash types:{Style.RESET_ALL}")
        for i, ht in enumerate(hash_types, 1):
            print(f"  {i}. {ht.upper()}")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}[?] Select hash type (1-{len(hash_types)}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(hash_types):
                    hash_type = hash_types[choice-1]
                    break
            except:
                pass
            print(f"{Fore.RED}[-] Invalid choice{Style.RESET_ALL}")
        
        # Get target hash
        target_hash = input(f"\n{Fore.YELLOW}[?] Enter target hash: {Style.RESET_ALL}").strip()
        if not target_hash:
            print(f"{Fore.RED}[-] Hash required{Style.RESET_ALL}")
            return
        
        # Get passwords
        passwords = self.get_passwords_input()
        if not passwords:
            print(f"{Fore.RED}[-] No passwords to try{Style.RESET_ALL}")
            return
        
        # Confirm this is YOUR hash
        print(f"\n{Fore.RED}[!] WARNING: Only crack hashes you created yourself!{Style.RESET_ALL}")
        confirm = input(f"{Fore.YELLOW}[?] Is this YOUR OWN hash? (yes/NO): {Style.RESET_ALL}").lower()
        if confirm != 'yes':
            print(f"{Fore.RED}[-] Aborting. Only test your own hashes.{Style.RESET_ALL}")
            return
        
        # Start cracking
        cracker = HashCracker(hash_type)
        result = cracker.crack(target_hash, passwords)
        
        # Display result
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        if result:
            print(f"{Fore.GREEN}[+] SUCCESS! Password found: {result}{Style.RESET_ALL}")
            
            # Test strength
            tester = PasswordStrengthTester()
            strength = tester.test_strength(result)
            print(f"{Fore.CYAN}[*] Password strength: {strength['color']}{strength['strength']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] Password not found in dictionary{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    def strength_test_mode(self):
        """Password strength testing mode"""
        print(f"\n{Fore.CYAN}═══ PASSWORD STRENGTH TESTER ═══{Style.RESET_ALL}")
        
        while True:
            password = input(f"\n{Fore.YELLOW}[?] Enter password to test (or 'back'): {Style.RESET_ALL}").strip()
            if password.lower() == 'back':
                return
            
            if not password:
                continue
            
            # Test strength
            tester = PasswordStrengthTester()
            result = tester.test_strength(password)
            
            # Display results
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Password Analysis:{Style.RESET_ALL}")
            print(f"  Length: {result['length']} characters")
            print(f"  Contains lowercase: {'✓' if result['has_lower'] else '✗'}")
            print(f"  Contains uppercase: {'✓' if result['has_upper'] else '✗'}")
            print(f"  Contains numbers: {'✓' if result['has_digit'] else '✗'}")
            print(f"  Contains special: {'✓' if result['has_special'] else '✗'}")
            print(f"\n  Strength: {result['color']}{result['strength']} ({result['score']}/10){Style.RESET_ALL}")
            
            if result['feedback']:
                print(f"\n{Fore.YELLOW}[!] Recommendations:{Style.RESET_ALL}")
                for fb in result['feedback']:
                    print(f"  • {fb}")
            
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            # Offer to test another
            again = input(f"\n{Fore.YELLOW}[?] Test another password? (yes/NO): {Style.RESET_ALL}").lower()
            if again != 'yes':
                break
    
    def dictionary_attack_mode(self):
        """Dictionary attack simulation"""
        print(f"\n{Fore.CYAN}═══ DICTIONARY ATTACK SIMULATION ═══{Style.RESET_ALL}")
        
        # Get target password (that you created)
        print(f"\n{Fore.YELLOW}[*] Create a test password for this simulation:{Style.RESET_ALL}")
        target_password = input(f"{Fore.YELLOW}[?] Enter a test password: {Style.RESET_ALL}").strip()
        
        if not target_password:
            print(f"{Fore.RED}[-] Password required{Style.RESET_ALL}")
            return
        
        # Hash the password for comparison
        target_hash = hashlib.md5(target_password.encode()).hexdigest()
        print(f"{Fore.CYAN}[*] Your password MD5 hash: {target_hash}{Style.RESET_ALL}")
        
        # Get dictionary file
        dict_file = input(f"\n{Fore.YELLOW}[?] Wordlist file [rockyou.txt]: {Style.RESET_ALL}").strip()
        if not dict_file:
            dict_file = "rockyou.txt"
        
        if not os.path.exists(dict_file):
            print(f"{Fore.YELLOW}[!] File not found. Using common passwords instead.{Style.RESET_ALL}")
            passwords = Config.COMMON_PASSWORDS + [target_password]
        else:
            passwords = PasswordGenerator.load_wordlist(dict_file)
            passwords.append(target_password)  # Ensure password is in list
        
        # Simulate attack
        print(f"\n{Fore.CYAN}[*] Starting dictionary attack simulation...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Testing {len(passwords)} passwords{Style.RESET_ALL}")
        
        start_time = time.time()
        found = False
        
        for i, password in enumerate(passwords, 1):
            # Calculate hash and compare
            hashed = hashlib.md5(password.encode()).hexdigest()
            
            if hashed == target_hash:
                found = True
                elapsed = time.time() - start_time
                print(f"\n{Fore.GREEN}[+] Password cracked: {password}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Attempts: {i}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Time: {elapsed:.2f} seconds{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Speed: {i/elapsed:.1f} passwords/sec{Style.RESET_ALL}")
                break
            
            # Progress every 1000 attempts
            if i % 1000 == 0:
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0
                print(f"\r{Fore.YELLOW}[*] Tried {i:,} passwords | {speed:.0f}/sec{Style.RESET_ALL}", end='')
        
        if not found:
            print(f"\n{Fore.YELLOW}[-] Password not found in dictionary{Style.RESET_ALL}")
        
        # Show what we learned
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] SECURITY LESSON:{Style.RESET_ALL}")
        print(f"  • Dictionary attacks are fast against weak passwords")
        print(f"  • Strong, unique passwords resist dictionary attacks")
        print(f"  • Use password managers to generate strong passwords")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    def brute_force_mode(self):
        """Brute force simulation (limited)"""
        print(f"\n{Fore.CYAN}═══ BRUTE FORCE SIMULATION ═══{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Warning: Full brute force is slow. This is a limited simulation.{Style.RESET_ALL}")
        
        # Get test password
        test_pass = input(f"\n{Fore.YELLOW}[?] Enter a SHORT test password (1-3 chars): {Style.RESET_ALL}").strip()
        
        if not test_pass:
            print(f"{Fore.RED}[-] Password required{Style.RESET_ALL}")
            return
        
        if len(test_pass) > 3:
            print(f"{Fore.RED}[!] Too long for simulation. Use 1-3 characters.{Style.RESET_ALL}")
            return
        
        # Generate combinations
        charset = string.ascii_lowercase + string.digits
        print(f"\n{Fore.CYAN}[*] Generating combinations for {len(test_pass)} characters...{Style.RESET_ALL}")
        
        passwords = []
        for length in range(1, len(test_pass) + 1):
            for combo in itertools.product(charset, repeat=length):
                passwords.append(''.join(combo))
        
        print(f"{Fore.CYAN}[*] Generated {len(passwords):,} combinations{Style.RESET_ALL}")
        
        # Simulate brute force
        print(f"{Fore.CYAN}[*] Starting brute force simulation...{Style.RESET_ALL}")
        
        start_time = time.time()
        found = False
        
        for i, password in enumerate(passwords, 1):
            if password == test_pass:
                found = True
                elapsed = time.time() - start_time
                print(f"\n{Fore.GREEN}[+] Password cracked: {password}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Attempts: {i}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Time: {elapsed:.4f} seconds{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Speed: {i/elapsed:.0f} attempts/sec{Style.RESET_ALL}")
                break
            
            # Progress
            if i % 1000 == 0:
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0
                print(f"\r{Fore.YELLOW}[*] Tried {i:,} combinations | {speed:.0f}/sec{Style.RESET_ALL}", end='')
        
        # Calculate total possibilities
        total_possible = len(charset) ** len(test_pass)
        print(f"\n{Fore.CYAN}[*] Total possible combinations: {total_possible:,}{Style.RESET_ALL}")
        
        # Security lesson
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] BRUTE FORCE MATHEMATICS:{Style.RESET_ALL}")
        print(f"  Password length: {len(test_pass)} chars")
        print(f"  Character set: {len(charset)} characters")
        print(f"  Possible combinations: {total_possible:,}")
        
        if len(test_pass) == 1:
            print(f"  Time to crack (at 1000/sec): ~{total_possible/1000:.1f} seconds")
        elif len(test_pass) == 2:
            print(f"  Time to crack (at 1000/sec): ~{total_possible/1000:.1f} seconds")
            print(f"  Time to crack (at 1M/sec): ~{total_possible/1000000:.2f} seconds")
        elif len(test_pass) == 3:
            print(f"  Time to crack (at 1M/sec): ~{total_possible/1000000:.1f} seconds")
            print(f"  Time to crack (at 1B/sec): ~{total_possible/1000000000:.2f} seconds")
        
        print(f"\n{Fore.CYAN}[*] SECURITY RECOMMENDATIONS:{Style.RESET_ALL}")
        print(f"  • Use at least 12 characters")
        print(f"  • Mix uppercase, lowercase, numbers, symbols")
        print(f"  • Each extra character exponentially increases security")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def personal_info_mode(self):
        """Attack based on personal information"""
        print(f"\n{Fore.CYAN}═══ PERSONAL INFORMATION ATTACK ═══{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] This shows how attackers use personal info to guess passwords{Style.RESET_ALL}")
        
        # Get personal information
        print(f"\n{Fore.YELLOW}[?] Enter YOUR OWN information (for educational demo):{Style.RESET_ALL}")
        full_name = input(f"{Fore.YELLOW}   Full name: {Style.RESET_ALL}").strip()
        birth_date = input(f"{Fore.YELLOW}   Birth date (DD-MM-YYYY): {Style.RESET_ALL}").strip()
        pet_name = input(f"{Fore.YELLOW}   Pet name (optional): {Style.RESET_ALL}").strip()
        city = input(f"{Fore.YELLOW}   City (optional): {Style.RESET_ALL}").strip()
        
        keywords = []
        if pet_name:
            keywords.append(pet_name)
        if city:
            keywords.append(city)
        
        # Create a test password from this info
        print(f"\n{Fore.YELLOW}[?] Create a test password using your info:{Style.RESET_ALL}")
        print(f"   Example: {full_name.split()[0].lower()}123")
        test_password = input(f"{Fore.YELLOW}   Your test password: {Style.RESET_ALL}").strip()
        
        if not test_password:
            print(f"{Fore.RED}[-] Password required{Style.RESET_ALL}")
            return
        
        # Generate passwords from personal info
        print(f"\n{Fore.CYAN}[*] Generating passwords from personal information...{Style.RESET_ALL}")
        generated = PasswordGenerator.generate_from_info(full_name, birth_date, keywords)
        generated.append(test_password)  # Ensure our test password is in the list
        
        # Add common variations
        for pwd in generated[:]:  # Copy list to avoid modification during iteration
            generated.append(pwd + "123")
            generated.append(pwd + "1234")
            generated.append(pwd + "!")
        
        generated = list(set(generated))  # Remove duplicates
        print(f"{Fore.CYAN}[*] Generated {len(generated)} potential passwords{Style.RESET_ALL}")
        
        # Show sample
        print(f"\n{Fore.YELLOW}[*] Sample generated passwords:{Style.RESET_ALL}")
        for pwd in generated[:15]:
            print(f"  - {pwd}")
        if len(generated) > 15:
            print(f"  - ... and {len(generated)-15} more")
        
        # Try to crack
        print(f"\n{Fore.CYAN}[*] Attempting to guess password...{Style.RESET_ALL}")
        
        start_time = time.time()
        found = False
        
        for i, password in enumerate(generated, 1):
            if password == test_password:
                found = True
                elapsed = time.time() - start_time
                print(f"\n{Fore.GREEN}[+] Password guessed: {password}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Attempts: {i}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Time: {elapsed:.2f} seconds{Style.RESET_ALL}")
                break
            
            if i % 100 == 0:
                elapsed = time.time() - start_time
                speed = i / elapsed if elapsed > 0 else 0
                print(f"\r{Fore.YELLOW}[*] Tried {i} passwords | {speed:.1f}/sec{Style.RESET_ALL}", end='')
        
        # Security lessons
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] PERSONAL INFORMATION SECURITY:{Style.RESET_ALL}")
        print(f"  • Attackers use personal info to guess passwords")
        print(f"  • Names, birth dates, pet names are common patterns")
        print(f"  • Social media leaks provide this information")
        
        print(f"\n{Fore.CYAN}[*] PROTECTION STRATEGIES:{Style.RESET_ALL}")
        print(f"  1. DON'T use personal info in passwords")
        print(f"  2. Use random password generators")
        print(f"  3. Enable two-factor authentication")
        print(f"  4. Use different passwords for each account")
        print(f"  5. Be careful what you share online")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def get_passwords_input(self):
        """Get passwords from user"""
        print(f"\n{Fore.YELLOW}[?] How do you want to provide passwords?{Style.RESET_ALL}")
        print(f"  1. Use common passwords list")
        print(f"  2. Load from wordlist file")
        print(f"  3. Enter manually (one per line, end with empty line)")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}[?] Select option (1-3): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                return Config.COMMON_PASSWORDS
            
            elif choice == '2':
                filename = input(f"{Fore.YELLOW}[?] Wordlist file [rockyou.txt]: {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "rockyou.txt"
                
                if not os.path.exists(filename):
                    print(f"{Fore.RED}[-] File not found: {filename}{Style.RESET_ALL}")
                    continue
                
                passwords = PasswordGenerator.load_wordlist(filename)
                print(f"{Fore.GREEN}[+] Loaded {len(passwords)} passwords{Style.RESET_ALL}")
                return passwords
            
            elif choice == '3':
                print(f"\n{Fore.YELLOW}[*] Enter passwords (one per line, empty line to finish):{Style.RESET_ALL}")
                passwords = []
                while True:
                    line = input(f"{Fore.CYAN}>> {Style.RESET_ALL}").strip()
                    if not line:
                        break
                    passwords.append(line)
                print(f"{Fore.GREEN}[+] Entered {len(passwords)} passwords{Style.RESET_ALL}")
                return passwords
            
            else:
                print(f"{Fore.RED}[-] Invalid choice{Style.RESET_ALL}")
    
    def run(self):
        """Main application loop"""
        while True:
            choice = self.display_menu()
            
            if choice == '0':
                print(f"\n{Fore.GREEN}[*] Thank you for learning about password security!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[*] Stay safe and use strong passwords!{Style.RESET_ALL}")
                break
            
            elif choice == '1':
                self.hash_cracking_mode()
            
            elif choice == '2':
                self.strength_test_mode()
            
            elif choice == '3':
                self.dictionary_attack_mode()
            
            elif choice == '4':
                self.brute_force_mode()
            
            elif choice == '5':
                self.personal_info_mode()
            
            # Pause before returning to menu
            if choice != '0':
                input(f"\n{Fore.YELLOW}[*] Press Enter to continue...{Style.RESET_ALL}")

# ==================== MAIN ====================
def main():
    """Entry point"""
    try:
        app = PasswordCrackerApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program interrupted{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
