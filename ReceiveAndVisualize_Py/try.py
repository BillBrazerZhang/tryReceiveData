import matplotlib.pyplot as plt
from stream_engine.stream import Stream, StreamAnimation


if __name__ == '__main__':
    from pylsl import StreamInlet, resolve_stream

    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    # Define a function that returns data. This function will be repetedly called.
    def imu_sampling():
        sample, timestamp = inlet.pull_sample()
        return [sample[0]]

    fig = plt.figure(figsize=(10, 3))
    ax1 = fig.add_subplot(111)
    ax1.set_xlim(0, 600)
    ax1.set_ylim(-100, 100)

    anim = StreamAnimation(fig, interval=100)  # Create a StreamAnimation object.
    anim.add_stream(Stream(ax1, imu_sampling))  # Add a Stream with a data function to it.

    plt.tight_layout()
    plt.show()