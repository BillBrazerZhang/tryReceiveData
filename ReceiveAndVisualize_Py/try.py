import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from stream_engine.stream import Stream, StreamAnimation
from scipy.ndimage.filters import gaussian_filter1d

base_style = {'figure.facecolor': '2d2d2d',
              'axes.facecolor': '404040',
              'axes.labelcolor': 'b0bdbb',
              'axes.prop_cycle': "cycler('color', ['74af60', '49b6d2', 'db4743', 'eba92b'])",
              'axes.grid': 'True',
              'grid.color': '343434',
              'grid.linestyle': '-',
              'grid.linewidth': '1.0',
              'text.color': 'b0bdbb',
              'xtick.color': 'efefef',
              'ytick.color': 'efefef'}

acc_style = [{'linestyle': '-', 'label': 'acc_x'},
             {'linestyle': '-', 'label': 'acc_y'},
             {'linestyle': '-', 'label': 'acc_z'}]

gyro_style = [{'label': 'gyro_x', 'color': '#F1A610'},
              {'label': 'gyro_y', 'color': '#F1108B'},
              {'label': 'gyro_z', 'color': '#10F1BE'}]


def config(*args):
    def x_format(x, pos):
        return '%1.0f' % abs(x/20)  # sampling rate; 20Hz

    for ax in args:
        ax.xaxis.set_major_formatter(FuncFormatter(x_format))
        ax.set_xlabel('Time (s)')

        leg = ax.legend(loc=9, ncol=6, framealpha=.2)
        for text in leg.get_texts():
            text.set_color('w')


with plt.style.context(base_style):
    fig = plt.figure(figsize=(10, 9))
    ax1 = fig.add_subplot(321)
    ax1.set_title('3-DoF accelerometer data of IMU 1')
    ax1.set_ylabel('Acceleration (m/s2)')
    ax1.set_xlim(0, 1000)
    ax1.set_ylim(-25, 100)
    ax2 = fig.add_subplot(322)
    ax2.set_title('3-DoF gyroscope data of IMU 1')
    ax2.set_ylabel('Angular velocity (rad/s)')
    ax2.set_xlim(0, 1000)
    ax2.set_ylim(0, 200)
    ax3 = fig.add_subplot(323)
    ax3.set_title('3-DoF accelerometer data of IMU 2')
    ax3.set_ylabel('Acceleration (m/s2)')
    ax3.set_xlim(0, 1000)
    ax3.set_ylim(-25, 100)
    ax4 = fig.add_subplot(324)
    ax4.set_title('3-DoF gyroscope data of IMU 2')
    ax4.set_ylabel('Angular velocity (rad/s)')
    ax4.set_xlim(0, 1000)
    ax4.set_ylim(0, 200)
    ax5 = fig.add_subplot(325)
    ax5.set_title('3-DoF accelerometer data of IMU 3')
    ax5.set_ylabel('Acceleration (m/s2)')
    ax5.set_xlim(0, 1000)
    ax5.set_ylim(-25, 100)
    ax6 = fig.add_subplot(326)
    ax6.set_title('3-DoF gyroscope data of IMU 3')
    ax6.set_ylabel('Angular velocity (rad/s)')
    ax6.set_xlim(0, 1000)
    ax6.set_ylim(0, 200)

if __name__ == '__main__':
    from pylsl import StreamInlet, resolve_stream

    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    sample = []
    timestamp = 0.0

    # Define a function that returns data. This function will be repetedly called.
    def imu1_acc_sampling():
        global sample, timestamp
        sample, timestamp = inlet.pull_sample()
        print("imu1: ", timestamp, sample)
        return [sample[0], sample[1], sample[2]]

    def imu1_gyro_sampling():
        return [sample[3], sample[4], sample[5]]


    def imu2_acc_sampling():
        return [sample[6], sample[7], sample[8]]


    def imu2_gyro_sampling():
        return [sample[9], sample[10], sample[11]]


    def imu3_acc_sampling():
        return [sample[12], sample[13], sample[14]]


    def imu3_gyro_sampling():
        return [sample[15], sample[16], sample[17]]

    # The default data processor
    def filter_proc(thread, data):
        thread['data'].appendleft(data)
        thread['line'].set_ydata(gaussian_filter1d(thread['data'], 3))  # apply a guassian filter to our data.
        return thread['line']


    imu1_acc_stream = Stream(ax1, imu1_acc_sampling, proc=filter_proc, style=acc_style)
    imu1_gyro_stream = Stream(ax2, imu1_gyro_sampling, proc=filter_proc, style=gyro_style)
    imu2_acc_stream = Stream(ax3, imu2_acc_sampling, proc=filter_proc, style=acc_style)
    imu2_gyro_stream = Stream(ax4, imu2_gyro_sampling, proc=filter_proc, style=gyro_style)
    imu3_acc_stream = Stream(ax5, imu3_acc_sampling, proc=filter_proc, style=acc_style)
    imu3_gyro_stream = Stream(ax6, imu3_gyro_sampling, proc=filter_proc, style=gyro_style)

    config(ax1, ax2, ax3, ax4, ax5, ax6)

    anim = StreamAnimation(fig, interval=1)  # Create a StreamAnimation object.
    anim.add_stream(imu1_acc_stream, imu1_gyro_stream, imu2_acc_stream,
                    imu2_gyro_stream, imu3_acc_stream, imu3_gyro_stream)  # Add a Stream with a data function to it.

    plt.tight_layout()
    plt.show()
