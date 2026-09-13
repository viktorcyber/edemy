import { PropsWithChildren } from "react";
import { useAuth, useUser } from '@clerk/expo'
import { useHostedAuth } from '@clerk/expo/hosted-auth'
import { ActivityIndicator, Button, StyleSheet, Text, View } from 'react-native'

export const CustomText = ({ children }: PropsWithChildren) => (
    <Text>{children}</Text>
);

export default function HomeScreen() {
  const { isLoaded, isSignedIn } = useAuth({ treatPendingAsSignedOut: false })
  const { startHostedAuth } = useHostedAuth()
  const { user } = useUser()

  const handleSignUp = async () => {
    try {
      await startHostedAuth({ mode: 'sign-up' })
    } catch (error) {
      // Handle the error in your app.
    }
  }

  if (!isLoaded) {
    return (
      <View className="flex flex-1 gap-3 items-center justify-center">
        <ActivityIndicator size="large" />
      </View>
    )
  }

  return (
    <View className="flex flex-1 gap-3 items-center justify-center">
      {isSignedIn ? (
        <CustomText>You're signed in</CustomText>
      ) : (
        <Button title="Sign up" onPress={handleSignUp} />
      )}
    </View>
  )
}