import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.ndimage import gaussian_filter1d

# Початкові константи
TIME = np.linspace( 0, 10, 1000 )

AMP_INIT = 1.0
FREQ_INIT = 1.0
PHASE_INIT = 0.0

NOISE_MEAN_INIT = 0.0
NOISE_COV_INIT = 0.01

GAUSS_SIGMA_INIT = 2.0

global_noise = np.random.normal( NOISE_MEAN_INIT, np.sqrt(NOISE_COV_INIT), size=TIME.shape )

# Функції генерації сигналу
def generate_clean_signal( t, amp, freq, phase ) :
    return amp * np.sin( freq * t + phase )

def generate_noisy_signal( clean_signal, noise_enabled ) :
    return clean_signal + global_noise if noise_enabled else clean_signal

# Фільтр Гауса
def gaussian_smooth_filter( signal, sigma ) :
    return gaussian_filter1d( signal, sigma )

# Оновлення шуму
def update_noise( val=None ) :
    global global_noise
    noise_mean = noise_mean_slider.val
    noise_cov = noise_cov_slider.val
    global_noise = np.random.normal( noise_mean, np.sqrt(noise_cov), size=TIME.shape )
    update_plot( )

# Оновлення графіків
def update_plot( val=None ) :
    amp = amp_slider.val
    freq = freq_slider.val
    phase = phase_slider.val
    sigma = gauss_sigma_slider.val
    show_noise = noise_check.get_status( )[ 0 ]

    clean_signal = generate_clean_signal( TIME, amp, freq, phase )
    noisy_signal = generate_noisy_signal( clean_signal, show_noise )
    filtered_signal = gaussian_smooth_filter( clean_signal + global_noise, sigma )

    plot_clean.set_ydata( clean_signal )
    plot_noisy.set_ydata( noisy_signal ) 
    plot_filtered.set_ydata( filtered_signal )
    fig.canvas.draw_idle( )

# Відновлення початкового стану
def reset_all( event ) :
    amp_slider.reset( )
    freq_slider.reset( )
    phase_slider.reset( )
    noise_mean_slider.reset( )
    noise_cov_slider.reset( )
    gauss_sigma_slider.reset( )

# Налаштування графіка та віджетів 
fig, ax = plt.subplots( figsize=(13, 6), facecolor='#2e2e2e' )
plt.subplots_adjust( bottom=0.37 )

# Початкові сигнали
clean_init = generate_clean_signal( TIME, AMP_INIT, FREQ_INIT, PHASE_INIT )
noisy_init = generate_noisy_signal( clean_init, True )
filtered_init = gaussian_smooth_filter( noisy_init, GAUSS_SIGMA_INIT )

plot_clean, = ax.plot( TIME, clean_init, color='#1abc9c', label='Чистий сигнал' )
plot_noisy, = ax.plot( TIME, noisy_init, color='#e67e22', label='Сигнал з шумом' )
plot_filtered, = ax.plot( TIME, filtered_init, color='#9b59b6', label='Фільтрований сигнал' )

ax.set_xlim( [0, 10] )
ax.set_ylim( [-2, 2] )
ax.legend( loc='upper right' )
ax.set_title( "Візуалізація сигналу з шумом та Гаусовим фільтром", fontsize=14, color='white' )
ax.set_xlabel( "Час", color='white' )
ax.set_ylabel( "Амплітуда", color='white' )
ax.tick_params( colors='white' )
ax.grid( True, color='#555555' )

slider_color = '#3c3c3c'
active_color = '#1abc9c'

def make_slider( axpos, label, valmin, valmax, valinit ) :
    ax_slider = plt.axes( axpos, facecolor=slider_color )
    slider = Slider( ax_slider, label, valmin, valmax, valinit=valinit, color=active_color )
    slider.label.set_color( 'white' )
    slider.valtext.set_color( 'white' )
    return slider

amp_slider = make_slider( [0.15, 0.26, 0.65, 0.03], 'Амплітуда', 0.1, 2.0, AMP_INIT )
freq_slider = make_slider( [0.15, 0.21, 0.65, 0.03], 'Частота', 0.1, 5.0, FREQ_INIT )
phase_slider = make_slider( [0.15, 0.16, 0.65, 0.03], 'Фаза', 0, 2 * np.pi, PHASE_INIT )

noise_mean_slider = make_slider( [0.15, 0.11, 0.65, 0.03], 'Середнє шуму', -1.0, 1.0, NOISE_MEAN_INIT )
noise_cov_slider = make_slider( [0.15, 0.06, 0.65, 0.03], 'Дисперсія шуму', 0.01, 1.0, NOISE_COV_INIT )

gauss_sigma_slider = make_slider( [0.15, 0.01, 0.65, 0.03], 'Sigma Гауса', 0.1, 10.0, GAUSS_SIGMA_INIT )

for slider in [ amp_slider, freq_slider, phase_slider, gauss_sigma_slider ] :
    slider.on_changed( update_plot )

for slider in [ noise_mean_slider, noise_cov_slider ] :
    slider.on_changed( update_noise )

# Чекбокс "Показати шум"
ax_checkbox = plt.axes( [0.86, 0.18, 0.11, 0.05], facecolor='#555555' )
noise_check = CheckButtons( ax_checkbox, ['Показати шум'], [True] )
for text in noise_check.labels :
    text.set_color( 'white' )
noise_check.on_clicked( update_plot )

# Кнопка "Скинути"
ax_reset = plt.axes( [0.86, 0.12, 0.11, 0.05], facecolor='#444444' )
reset_button = Button( ax_reset, 'Скинути', color='#555555', hovercolor='#777777' )
reset_button.label.set_color( 'white' )
reset_button.on_clicked( reset_all )

plt.show( )
