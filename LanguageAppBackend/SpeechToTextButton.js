import React, { useState } from "react";
import { View, StyleSheet, Pressable } from "react-native";
import { Audio } from "expo-av";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import * as FileSystem from "expo-file-system";
import { FLASK_BACKEND } from "@env";
import LoadingSign from "./LoadingSign";

function SpeechToTextButton({ getTranscription, languageCode }) {
  const [recording, setRecording] = useState();
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  async function startRecording() {
    setIsRecording(true);
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync({
        android: {
          extension: ".amr",
          audioEncoder: Audio.RECORDING_OPTION_ANDROID_AUDIO_ENCODER_AMR_WB,
          outputFormat: Audio.RECORDING_OPTION_ANDROID_OUTPUT_FORMAT_AMR_WB,
        },
        ios: {
          extension: ".amr",
          sampleRate: 44100,
          numberOfChannels: 2,
          bitRate: 128000,
          audioQuality: Audio.RECORDING_OPTION_IOS_AUDIO_QUALITY_HIGH,
          outputFormat: Audio.RECORDING_OPTION_IOS_OUTPUT_FORMAT_AMR_WB,
        },
      });
      setRecording(recording);
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  }

  async function stopRecording() {
    setIsRecording(false);
    setRecording(undefined);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();

    setIsProcessing(true);
    try {
      const api = FLASK_BACKEND + languageCode;
      const response = await FileSystem.uploadAsync(api, uri);
      console.log(response);
      const body = JSON.parse(response.body);
      console.log(body.text);
      getTranscription(body.text);
    } catch (err) {
      console.error("Failed to stop recording", err);
    }
    setIsProcessing(false);
  }

  return (
    <View style={styles.container}>
      <Pressable
        onPressIn={startRecording}
        onPressOut={stopRecording}
        style={[styles.button, isRecording && styles.dim]}
      >
        <View style={styles.icon}>
          {isProcessing ? (
            <LoadingSign />
          ) : (
            <MaterialCommunityIcons name="microphone" size={40} />
          )}
        </View>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  button: {
    width: 70,
    height: 70,
    backgroundColor: "white",
    borderRadius: 50,
    borderColor: "black",
    borderWidth: 3,
  },
  dim: {
    opacity: 0.2,
  },
  icon: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});

export default SpeechToTextButton;
