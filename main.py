from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import numpy as np

# Fungsi untuk menghitung statistik lengkap
def calculate_detailed_stats(samples):
    data = np.array(samples)
    n = len(data)
    mean = np.mean(data)
    variance = np.var(data, ddof=1)  # Variansi dengan ddof=1 untuk sampel
    std_dev = np.sqrt(variance)  # Simpangan baku
    coeff_variance = std_dev / mean  # Koefisien variasi
    std_error = std_dev / np.sqrt(n)  # Standard Error of Mean
    
    sum_squared_diff = np.sum((data - mean) ** 2)  # Jumlah kuadrat selisih
    solution_table = [(x, x - mean, (x - mean) ** 2) for x in data]  # Tabel xᵢ, xᵢ - x̄, (xᵢ - x̄)²
    
    results = {
        "n": n,
        "sum": np.sum(data),
        "mean": mean,
        "variance": variance,
        "std_dev": std_dev,
        "coeff_variance": coeff_variance,
        "std_error": std_error,
        "sum_squared_diff": sum_squared_diff,
        "solution_table": solution_table,
    }
    return results

# Fungsi untuk menangani input sampel dari pengguna
async def handle_samples(update: Update, context):
    message = update.message.text
    
    # Parsing input menjadi daftar float
    try:
        samples = list(map(float, message.split(',')))
    except ValueError:
        await update.message.reply_text("Format salah. Pastikan angka dipisahkan dengan koma.")
        return
    
    # Menghitung hasil
    results = calculate_detailed_stats(samples)
    
    # Membuat output dengan Markdown
    response = (
        f"*Count (n)*: {results['n']}\n"
        f"*Sum (Σx)*: {results['sum']:.2f}\n"
        f"*Mean (x̄)*: {results['mean']:.3f}\n"
        f"*Variance (s²)*: {results['variance']:.2f}\n"
        f"*Coefficient Of Variance*: {results['coeff_variance']:.4f}\n"
        f"*Standard Error of Mean (SE)*: {results['std_error']:.10f}\n"
        f"\n*Solution*:\n"
        f"s = Σᵢ=₁ⁿ (xᵢ - x̄)² / (n-1)\n"
        f"s = {results['sum_squared_diff']:.6f} / {results['n'] - 1}\n"
        f"s = {results['variance']:.6f}\n"
        f"s = √{results['variance']:.6f} = {results['std_dev']:.4f}\n\n"
        f"xᵢ\t xᵢ - x̄\t (xᵢ - x̄)²\n"
    )
    
    # Menambahkan tabel solusi ke dalam output
    for row in results['solution_table']:
        response += f"{row[0]:.2f}\t {row[1]:.3f}\t {row[2]:.6f}\n"
    
    response += f"Σxᵢ = {results['sum']:.2f}\t\t Σ(xᵢ - x̄)² = {results['sum_squared_diff']:.6f}\n"
    
    # Mengirim balasan ke pengguna dengan format Markdown
    await update.message.reply_text(response, parse_mode="Markdown")

# Fungsi untuk memulai bot
async def start(update: Update, context):
    await update.message.reply_text("Masukkan sampel dengan format: 6.8, 7.2, 6.9, ...")

# Fungsi untuk memberikan bantuan
async def help_command(update: Update, context):
    help_text = (
        "Saya dapat membantu Anda menghitung nilai statistik!\n"
        "Masukkan sampel angka dalam format: `6.8, 7.2, 6.9, ...`\n"
        "Saya akan menghitung:\n"
        "- Jumlah data (n)\n"
        "- Jumlah total (Σx)\n"
        "- Rata-rata (x̄)\n"
        "- Variansi (s²)\n"
        "- Koefisien Variasi\n"
        "- Standard Error of Mean (SE)\n\n"
        "Gunakan perintah /start untuk memulai!"
    )
    await update.message.reply_text(help_text)

# Fungsi utama untuk menjalankan bot
def main():
    # Masukkan token bot Anda di sini
    TOKEN = "7567580368:AAECOmANp17o-jcGj2CeWU1Zef_OPXBHjM8"

    # Buat aplikasi bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Daftarkan command dan handler pesan
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_samples))

    # Jalankan bot
    app.run_polling()

if __name__ == "__main__":
    main()
