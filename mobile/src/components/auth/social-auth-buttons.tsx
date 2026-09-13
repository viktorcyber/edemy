import { useSignInWithApple } from '@clerk/expo/apple';
import { useSignInWithGoogle } from '@clerk/expo/google';
import { Button, Host } from '@expo/ui';
import { useRouter } from 'expo-router';
import { Alert, Platform, View } from 'react-native';

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === 'object' && error !== null && 'message' in error) {
    return String(error.message);
  }

  return 'Unable to complete social sign-in. Please try again.';
}

export function SocialAuthButtons() {
  const router = useRouter();
  const { startGoogleAuthenticationFlow } = useSignInWithGoogle();
  const { startAppleAuthenticationFlow } = useSignInWithApple();

  const handleGooglePress = async () => {
    try {
      const { createdSessionId, setActive } = await startGoogleAuthenticationFlow();

      if (createdSessionId && setActive) {
        await setActive({ session: createdSessionId });
        router.replace('/');
      }
    } catch (error) {
      if (typeof error === 'object' && error !== null && 'code' in error) {
        const code = String(error.code);
        if (code === 'SIGN_IN_CANCELLED' || code === '-5') {
          return;
        }
      }

      Alert.alert('Google sign-in failed', getErrorMessage(error));
    }
  };

  const handleApplePress = async () => {
    try {
      const { createdSessionId, setActive } = await startAppleAuthenticationFlow();

      if (createdSessionId && setActive) {
        await setActive({ session: createdSessionId });
        router.replace('/');
      }
    } catch (error) {
      if (
        typeof error === 'object' &&
        error !== null &&
        'code' in error &&
        String(error.code) === 'ERR_REQUEST_CANCELED'
      ) {
        return;
      }

      Alert.alert('Apple sign-in failed', getErrorMessage(error));
    }
  };

  return (
    <View className="gap-3">
      <Host matchContents={false} style={{ width: '100%' }}>
        <Button
          label="Continue with Google"
          onPress={() => void handleGooglePress()}
          variant="outlined"
          style={{ width: '100%', height: 52, borderRadius: 16 }}
        />
      </Host>

      {Platform.OS === 'ios' ? (
        <Host matchContents={false} style={{ width: '100%' }}>
          <Button
            label="Continue with Apple"
            onPress={() => void handleApplePress()}
            variant="outlined"
            style={{ width: '100%', height: 52, borderRadius: 16 }}
          />
        </Host>
      ) : null}
    </View>
  );
}
