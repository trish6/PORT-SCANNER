import socket
import threading
from colorama import Fore, Style, init

init(autoreset=True)
results = []

def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        try:
            banner = s.recv(1024).decode().strip()
            banner_text = banner if banner else "No banner"
        except:
            banner_text = "Banner grab failed"
        
        result = f"OPEN, Port {port}, Banner: {banner_text}"
        print(Fore.GREEN + f"[OPEN]   Port {port} | Banner: {banner_text}" + Style.RESET_ALL)
        results.append(result)
        s.close()
    except Exception as e:
        result = f"CLOSED, Port {port}, Error: {e}"
        print(Fore.RED + f"[CLOSED] Port {port} - {e}" + Style.RESET_ALL)
        results.append(result)

def save_results_text(filename):
    with open(filename, "w") as f:
        for line in results:
            f.write(line + "\n")

def save_results_html(filename, chart_type="bar"):
    open_count = sum(1 for r in results if r.startswith("OPEN"))
    closed_count = sum(1 for r in results if r.startswith("CLOSED"))

    html_header = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Port Scan Results</title>
<style>
    body {{
        background-color: #000;
        color: #eee;
        font-family: Arial, sans-serif;
        padding: 20px;
    }}
    h1 {{
        color: #fff;
        font-weight: bold;
        text-align: center;
    }}
    .open {{
        color: #4ade80;  /* bright green */
        background-color: #022c22;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 8px;
    }}
    .closed {{
        color: #f87171;  /* soft red */
        background-color: #2c0000;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 8px;
    }}
    #chart-container {{
        width: 60%;
        margin: 30px auto;
        background-color: #111;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px #0ff;
    }}
</style>
</head>
<body>
<h1>Port Scan Results</h1>

<div id="chart-container">
    <canvas id="portChart"></canvas>
</div>

<div>
"""
    html_footer = f"""
</div>

<!-- Chart.js library -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('portChart').getContext('2d');
const portChart = new Chart(ctx, {{
    type: '{chart_type}',
    data: {{
        labels: ['Open Ports', 'Closed Ports'],
        datasets: [{{
            label: 'Number of Ports',
            data: [{open_count}, {closed_count}],
            backgroundColor: [
                'rgba(74, 222, 128, 0.7)',  // green
                'rgba(248, 113, 113, 0.7)'   // red
            ],
            borderColor: [
                'rgba(74, 222, 128, 1)',
                'rgba(248, 113, 113, 1)'
            ],
            borderWidth: 1
        }}]
    }},
    options: {{
        scales: {{
            y: {{
                beginAtZero: true,
                precision: 0,
                ticks: {{
                    color: '#eee'
                }},
                grid: {{
                    color: '#333'
                }}
            }},
            x: {{
                ticks: {{
                    color: '#eee'
                }},
                grid: {{
                    color: '#333'
                }}
            }}
        }},
        plugins: {{
            legend: {{
                labels: {{
                    color: '#eee'
                }}
            }}
        }}
    }}
}});
</script>

</body>
</html>"""

    with open(filename, "w") as f:
        f.write(html_header)
        for line in results:
            if line.startswith("OPEN"):
                f.write(f'<div class="open">{line}</div>\n')
            else:
                f.write(f'<div class="closed">{line}</div>\n')
        f.write(html_footer)

def main():
    ip = input("Enter IP address to scan: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    text_file = "scan_results.txt"
    html_file = "scan_results.html"

    save_results_text(text_file)
    save_results_html(html_file)  # Always bar chart now

    print(Fore.CYAN + f"\nScan complete. Results saved to '{text_file}' and '{html_file}'." + Style.RESET_ALL)
    print(f"Open '{html_file}' in your browser to view the results.")

if __name__ == "__main__":
    main()
