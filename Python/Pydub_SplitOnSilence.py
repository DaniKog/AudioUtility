
import sys
import os
aegumentName = "File Name (String), Min Silecne Length (ms), Silecne Threshold (dBFS), Silinece Padding (ms)"
# Setup the arguments
lArguments = sys.argv
# Setup defualt values
a_min_silence_len = 1500;
a_silence_thresh = -40;
a_silence_chunk = 500;

if len(lArguments) == 1 :
	print("Empty list of arguments please speifiy")
	print(aegumentName)
	sys.exit()
elif  len(lArguments) == 2 :
	print("Not all arguments are filled in using default values")
	a_filename = lArguments[1]
else:
	a_filename = lArguments[1]
	
	if lArguments[2] != None:
		a_min_silence_len = int(lArguments[2])
	else:
		print("Min Silecne Length is not filled in will use default value")
	
	if lArguments[3] != None:
		a_silence_thresh = int(lArguments[3])
	else:
		print("Silecne Threshold is not filled in will use default value")
		
	if lArguments[4] != None:
		a_silence_chunk = int(lArguments[4])
	else:
		print("Silinece Padding is not filled in will use default value")	

#print out before running
print("---------------------------------------------------")
print("Starting to split", str(a_filename), "With Varibles")
print("Min Silecne Length",a_min_silence_len)
print("Silecne Threshold",a_silence_thresh)
print("Silinece Padding",a_silence_chunk)

# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

print("Loading File Please Wait")
# Load your audio.
song = AudioSegment.from_wav(a_filename)
# Split track where the silence is 3 seconds or more and get chunks using the imported function.
chunks = split_on_silence (
    # Use the loaded audio.
    song, 
    # Specify that a silent chunk must be at least 3 seconds or 2000 ms long.
    a_min_silence_len,
    # Consider a chunk silent if it's quieter than -16 dBFS.
    # (You may want to adjust this parameter.)
    a_silence_thresh
)
# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    silence_chunk = AudioSegment.silent(a_silence_chunk)
	
    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk
    # Normalize the entire chunk.
    # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    fileName, ext = os.path.splitext(a_filename)
    print("Exporting {0}_{1}.wav.".format(fileName,i))
    audio_chunk.export(
        ".//{0}_{1}.wav".format(fileName,i),
        bitrate = "192k",
        format = "wav"
    )
