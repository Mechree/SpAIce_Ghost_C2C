#!/usr/bin/env python
# coding: utf-8

# In[ ]:

######################## WORKING PROGRAM ######################## WORKING PROGRAM #########################
# Libraries
import requests
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip
import webbrowser
import time
import os
from mutagen.mp3 import MP3
import openai
import random

######## FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS FUNCTIONS #######
# Generate character text response
def get_response_from_gpt3(prompt, api_key, character):
    openai.api_key = api_key
    system_message = f"You are {character}. Keep responses between one to three sentences and try to be humorous or witty. Avoid conveying gestures with asteriks. Do not begin sentences with 'Well,' ."
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
      ]
    )
    return response['choices'][0]['message']['content'].strip()


# Generate voices from generated text response
def create_mp3_from_text(conversation, output_file, model_id, voice_id, stab, sim):

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/"+voice_id +"/stream"
    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": "40a..."
        
    }

    data = {
      "text": conversation,
      "model_id": model_id,
      "voice_settings": {
        "stability": stab,
        "similarity_boost": sim
      }
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Create video
def combine_audio_and_video(video_file, audio_file, output_file, i):

    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    # Loop the video for the duration of the audio
    video = video.loop(duration=audio.duration)

    video_with_audio = video.set_audio(audio)
    
    output_file_unique = output_file.split(".mp4")[0] + str(i) + ".mp4"
    video_with_audio.write_videofile(output_file_unique, codec='libx265')

    return output_file_unique

# Use this to add intros or endings
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_videos(video1_path, video2_path, output_path):
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    final_video = concatenate_videoclips([video1, video2])
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
    # Intro Video Location
# video1_path = r'\SPACEGHOST AI PROJECT\scenes\SceneIntro.mp4'
    # Completed Video Location
# video2_path = r'\SPACEGHOST AI PROJECT\Genereated Content\FinalVersions\Pilot.mp4'
    # Output Location
# output_path = r'\SPACEGHOST AI PROJECT\Genereated Content\FinalVersions\PilotNew.mp4'

# concatenate_videos(video1_path, video2_path, output_path)


#Play and Close video with sound
def play_and_close_video(video_file):
    # Get the duration of the video
    video = VideoFileClip(video_file)
    duration = video.duration

    # Open the video file
    webbrowser.open(video_file)

    # Wait for the video to finish playing
    time.sleep(duration)

    # Close the application
    os.system("taskkill /IM vlc.exe /F")

# Generate Talk Show
def run_talkshow(numLoops, guestAPI, guest, topicResponse, guestVoiceID, guestStab, guestSim, include_guest):

    # APIs and Character Initializers
    moltarAPI = "sk-S..."
    moltarVoiceID = "NOv..."
    moltarStab = 0.75
    moltarSim = 0.75
    sgAPI = "sk-7..."
    sgVoiceID = "FK7..."
    sgStab = 0.13
    sgSim = 0.40
    zorakAPI = "sk-N..."
    zorakVoiceID = "D8B..."
    zkStab = 0.38
    zkSim = 0.95
    model_id = "eleven_monolingual_v1"

    # Define character-specific parameters
    speakerIDs = [sgVoiceID, moltarVoiceID, zorakVoiceID]
    speakerStabs = [sgStab, moltarStab, zkStab]
    speakerSims = [sgSim, moltarSim, zkSim]
    scenes = [sgScenes, mtScenes, zkScenes]
    
    # Other Initializers
    closePrompt = " Respond without using your own name at the beginning of the sentence, do not be repetitive and do not repeat what the previous prompts say."
    host = "Space Ghost on his talkshow Coast to Coast"
    moltar = "Moltar from Space Ghost Coast to Coast"
    zorak = "Zorak from Space Ghost Coast to Coast"
    
    # Add Moltar and Zorak
    characters = [host, moltar, zorak]
    APIs = [sgAPI, moltarAPI, zorakAPI]
    
    if include_guest:
        speakerIDs.append(guestVoiceID)
        speakerStabs.append(guestStab)
        speakerSims.append(guestSim)
        scenes.append([guestScene])
        characters.append(guest)
        APIs.append(guestAPI)

# list to store paths of generated video files
    video_files = []  
    
 # Opening Act
    if include_guest:
        sgPrompt =  "Start the show off by saying 'Greetings I'm Space Ghost. Welcome to the show!' Introduce" + guest + " make an snarky comment about them, and then ask them about " + topicResponse + "."
    else:
        sgPrompt =  "Start the show off by saying 'Greetings I'm Space Ghost. Welcome to the show!' Start talking about " + topicResponse + "."
    
    response = get_response_from_gpt3(sgPrompt, sgAPI, "Space Ghost")
    print("Space Ghost Intro: " , response)
    last_speaker = host
    print()
    print("Generating scene...")
    print()
    
    # Generate audio and video for Space Ghost's opening
    create_mp3_from_text(response, 'sg_audio_0.mp3', model_id, sgVoiceID, sgStab, sgSim)
    video_files.append(combine_audio_and_video(sgScene, 'sg_audio_0.mp3', 'sg_video_0.mp4', 0))
    
    # Conversation 
    if include_guest:
        prompt = last_speaker + " just said to you " + response + closePrompt
        response = get_response_from_gpt3(prompt, guestAPI, guest)
        print(guest ,": ", response)
        last_speaker = guest
        print()
        # Generate audio and video for the guest's response
        create_mp3_from_text(response, 'guest_audio_0.mp3', model_id, guestVoiceID, guestStab, guestSim)
        video_files.append(combine_audio_and_video(guestScene, 'guest_audio_0.mp3', 'guest_video_0.mp4', 0))
        print()
    
    # Conversations with Interviewer
    for i in range (numLoops):
        print("Interview " + str(i) + " loop.")
        print()
    
        # Choose a random character to speak, but not the same one twice in a row
        speaker = last_speaker
        while speaker == last_speaker:
            speaker = random.choice(characters)
    
        speaker_index = characters.index(speaker)
        
        #if include_guest and speaker == host:
            #prompt = last_speaker + " just said to you " + response + "Ask " + guest+ " about " + topic + closePrompt
        #else:
        prompt = last_speaker + " just said to you " + response + closePrompt
            
        response = get_response_from_gpt3(prompt, APIs[speaker_index], speaker)

        print(speaker + ":", response)
        print()
        
        # Choose a random scene for the character
        scene = random.choice(scenes[speaker_index])
        print()
        print(scene)
        print()

        # Generate audio and video for the current speaker
        create_mp3_from_text(response, f'{speaker}_audio_{i+1}.mp3', model_id, speakerIDs[speaker_index], speakerStabs[speaker_index], speakerSims[speaker_index])
        video_files.append(combine_audio_and_video(scene, f'{speaker}_audio_{i+1}.mp3', f'{speaker}_video_{i+1}.mp4', i+1))
    
        # Remember who just spoke
        last_speaker = speaker
    
    # Space Ghost wraps up the show
    if last_speaker == host:
        sgPrompt = "It's time to wrap up the show. End the show properly and say goodbye to the viewers." + closePrompt 
    else:
        sgPrompt = "It's time to wrap up the show. End the show properly and say goodbye to the viewers."  + last_speaker + " just said to you " + response + closePrompt 
    response = get_response_from_gpt3(sgPrompt, sgAPI, "Space Ghost")
    print(host + ":", response)
        
    # Generate audio and video for Space Ghost's closing
    create_mp3_from_text(response, 'sg_audio_final.mp3', model_id, sgVoiceID, sgStab, sgSim)
    video_files.append(combine_audio_and_video(sgScene, 'sg_audio_final.mp3', 'sg_video_final.mp4', numLoops+1))

    return video_files  # return the list of generated video files

####### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ########

# Seed the random number generator with the current time
random.seed(time.time())

# SCENES
    # Guest
guestScene = r"SPACEGHOST AI PROJECT\scenes\DavidAttTalking.mp4"

    # Intros
introScenes = [
    r"\SPACEGHOST AI PROJECT\scenes\SceneIntro.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SceneIntro2.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SceneIntro3.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SceneIntro4.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SceneIntro5.mp4"
]
    # Select Intro Scene
introScene = introScenes[random.randint(0,len(introScenes) -1)]
introClip = VideoFileClip(introScene)
print("Intro Scene: ", introScene)

    # Moltar
mtScenes = [r"\SPACEGHOST AI PROJECT\scenes\MoltarTalk1.mp4", 
            r"\SPACEGHOST AI PROJECT\scenes\MoltarTalk2.mp4" ] 
    # Select Moltar Scene
mtScene = mtScenes[random.randint(0, len(mtScenes) - 1)]

    # Space Ghost
sgScenes = [
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk2.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk3.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk4.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk5.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk6.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk7.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk8.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk9.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\SpaceGhostTalk10.mp4"
]
    # Select Space Ghost Scene
sgScene = sgScenes[random.randint(0, len(sgScenes) - 1)]
print ("Opening Scene: ", sgScene)
print()

    # Zorak
zkScenes = [
    r"\SPACEGHOST AI PROJECT\scenes\ZorakTalk1.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\ZorakTalk3.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\ZorakTalk4.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\ZorakTalk5.mp4",
    r"\SPACEGHOST AI PROJECT\scenes\ZorakTalk6.mp4"
]
    # Select Zorak Scene
zkScene = zkScenes[random.randint(0, len(zkScenes) -1)]

    # Ending change 
cgScenes = [
    r"\SPACEGHOST AI PROJECT\scenes\SceneChange1.mp4"
]

######## INITIALIZERS INITIALIZERS INITIALIZERS INITIALIZERS INITIALIZERS #######

# Define Parameters for guest and topic
guestAPI = "sk-...."
guest = "Sir David Attenborough"
guestVoiceID = "5wJ..."
guestStab = .50
guestSim = .85
topic = "Insert Topic Here"

# Store paths to final clips
final_clips = []

###### Call the function to run the talk show ######
video_files = run_talkshow(12, guestAPI, guest , topic , guestVoiceID, guestStab, guestSim, True)

# Add Clips

for video_file in video_files:
    clip = VideoFileClip(video_file)
    final_clips.append(clip)

# Create a VideoFileClip of the chosen cgScene
cgScene = cgScenes[random.randint(0, len(cgScenes) -1)]
cgClip = VideoFileClip(cgScene)

# Append the cgClip to final_clips
final_clips.append(cgClip)

# Insert intro clip 
final_clips = [introClip] + final_clips

# Combine video files
final_video = concatenate_videoclips(final_clips)
final_video_file = r'\SPACEGHOST AI PROJECT\Genereated Content\final_output.mp4'
final_video.write_videofile(final_video_file, codec='libx265')

# Play and close
play_and_close_video(final_video_file)

##### END PROGRAM #####
