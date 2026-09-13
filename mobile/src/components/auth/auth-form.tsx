import { useSignIn, useSignUp } from '@clerk/expo';
import { Button, Host } from '@expo/ui';
import { Href, Link, useRouter } from 'expo-router';
import { useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View,
} from 'react-native';

import { SocialAuthButtons } from './social-auth-buttons';

type AuthMode = 'sign-in' | 'sign-up';

function getClerkErrorMessage(error: unknown) {
  if (typeof error === 'object' && error !== null && 'errors' in error) {
    const errors = error.errors;
    if (Array.isArray(errors) && errors[0] && typeof errors[0] === 'object') {
      const firstError = errors[0] as { longMessage?: string; message?: string };
      return firstError.longMessage ?? firstError.message ?? 'Something went wrong.';
    }
  }

  return 'Something went wrong. Please check your details and try again.';
}

function Field({
  label,
  value,
  onChangeText,
  placeholder,
  secureTextEntry = false,
  keyboardType,
  autoCapitalize = 'none',
}: {
  label: string;
  value: string;
  onChangeText: (value: string) => void;
  placeholder: string;
  secureTextEntry?: boolean;
  keyboardType?: 'default' | 'email-address';
  autoCapitalize?: 'none' | 'words';
}) {
  return (
    <View className="gap-2">
      <Text className="text-sm font-semibold text-slate-700">{label}</Text>
      <TextInput
        className="h-14 rounded-2xl border border-slate-200 bg-white px-4 text-base text-slate-950"
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="#94a3b8"
        secureTextEntry={secureTextEntry}
        keyboardType={keyboardType}
        autoCapitalize={autoCapitalize}
        autoCorrect={false}
      />
    </View>
  );
}

export function AuthForm({ mode }: { mode: AuthMode }) {
  const router = useRouter();
  const isSignUp = mode === 'sign-up';
  const { signIn, fetchStatus: signInFetchStatus } = useSignIn();
  const { signUp, fetchStatus: signUpFetchStatus } = useSignUp();
  const [emailAddress, setEmailAddress] = useState('');
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isVerificationStep, setIsVerificationStep] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const fetchStatus = isSignUp ? signUpFetchStatus : signInFetchStatus;
  const isSubmitting = fetchStatus === 'fetching';

  const navigateHome = () => {
    router.replace('/' as Href);
  };

  const handleSubmit = async () => {
    setErrorMessage('');

    if (!emailAddress.trim() || !password) {
      setErrorMessage('Enter your email and password to continue.');
      return;
    }

    try {
      if (isSignUp) {
        const { error } = await signUp.password({
          emailAddress: emailAddress.trim(),
          password,
        });

        if (error) {
          setErrorMessage(getClerkErrorMessage(error));
          return;
        }

        await signUp.verifications.sendEmailCode();
        setIsVerificationStep(true);
        return;
      }

      const { error } = await signIn.password({
        emailAddress: emailAddress.trim(),
        password,
      });

      if (error) {
        setErrorMessage(getClerkErrorMessage(error));
        return;
      }

      if (signIn.status === 'complete') {
        await signIn.finalize({ navigate: navigateHome });
      } else {
        setErrorMessage('Additional verification is required for this account.');
      }
    } catch (error) {
      setErrorMessage(getClerkErrorMessage(error));
    }
  };

  const handleVerifyEmail = async () => {
    setErrorMessage('');

    if (!verificationCode.trim()) {
      setErrorMessage('Enter the verification code from your email.');
      return;
    }

    try {
      const { error } = await signUp.verifications.verifyEmailCode({
        code: verificationCode.trim(),
      });

      if (error) {
        setErrorMessage(getClerkErrorMessage(error));
        return;
      }

      if (signUp.status === 'complete') {
        await signUp.finalize({ navigate: navigateHome });
      }
    } catch (error) {
      setErrorMessage(getClerkErrorMessage(error));
    }
  };

  return (
    <ScrollView
      className="flex-1 bg-slate-50"
      contentContainerClassName="grow px-6 pb-10 pt-16"
      keyboardShouldPersistTaps="handled">
      <View className="flex-1 justify-between">
        <View className="gap-8">
          <View className="gap-4">
            <View className="h-12 w-12 items-center justify-center rounded-2xl bg-indigo-600">
              <Text className="text-xl font-bold text-white">E</Text>
            </View>
            <View className="gap-2">
              <Text className="text-4xl font-bold tracking-tight text-slate-950">
                {isVerificationStep ? 'Check your inbox' : isSignUp ? 'Start learning smarter' : 'Welcome back'}
              </Text>
              <Text className="text-base leading-6 text-slate-500">
                {isVerificationStep
                  ? `We sent a verification code to ${emailAddress}.`
                  : isSignUp
                    ? 'Create your Edemy account and make progress every day.'
                    : 'Sign in to continue your learning journey.'}
              </Text>
            </View>
          </View>

          {isVerificationStep ? (
            <View className="gap-5">
              <Field
                label="Verification code"
                value={verificationCode}
                onChangeText={setVerificationCode}
                placeholder="000000"
                keyboardType="default"
                autoCapitalize="none"
              />
              <Host matchContents={false} style={{ width: '100%' }}>
                <Button
                  label="Verify email"
                  onPress={() => void handleVerifyEmail()}
                  disabled={isSubmitting}
                  style={{ width: '100%', height: 56, borderRadius: 18 }}
                />
              </Host>
              <Pressable onPress={() => setIsVerificationStep(false)}>
                <Text className="text-center font-semibold text-indigo-600">Use a different email</Text>
              </Pressable>
            </View>
          ) : (
            <View className="gap-5">
              <SocialAuthButtons />
              <View className="flex-row items-center gap-3">
                <View className="h-px flex-1 bg-slate-200" />
                <Text className="text-xs font-semibold uppercase tracking-widest text-slate-400">or</Text>
                <View className="h-px flex-1 bg-slate-200" />
              </View>
              <Field
                label="Email address"
                value={emailAddress}
                onChangeText={setEmailAddress}
                placeholder="you@example.com"
                keyboardType="email-address"
              />
              <View className="gap-2">
                <View className="flex-row items-center justify-between">
                  <Text className="text-sm font-semibold text-slate-700">Password</Text>
                  {!isSignUp ? (
                    <Pressable>
                      <Text className="text-sm font-semibold text-indigo-600">Forgot password?</Text>
                    </Pressable>
                  ) : null}
                </View>
                <View className="flex-row items-center rounded-2xl border border-slate-200 bg-white">
                  <TextInput
                    className="h-14 flex-1 px-4 text-base text-slate-950"
                    value={password}
                    onChangeText={setPassword}
                    placeholder="Your password"
                    placeholderTextColor="#94a3b8"
                    secureTextEntry={!showPassword}
                    autoCapitalize="none"
                    autoCorrect={false}
                  />
                  <Pressable className="px-4" onPress={() => setShowPassword((visible) => !visible)}>
                    <Text className="text-sm font-semibold text-indigo-600">{showPassword ? 'Hide' : 'Show'}</Text>
                  </Pressable>
                </View>
              </View>
              {errorMessage ? <Text className="text-sm leading-5 text-red-600">{errorMessage}</Text> : null}
              <Host matchContents={false} style={{ width: '100%' }}>
                <Button
                  label={isSignUp ? 'Create account' : 'Sign in'}
                  onPress={() => void handleSubmit()}
                  disabled={isSubmitting}
                  style={{ width: '100%', height: 56, borderRadius: 18 }}
                />
              </Host>
              {isSignUp ? <View nativeID="clerk-captcha" /> : null}
            </View>
          )}
        </View>

        <View className="mt-12 flex-row justify-center gap-1">
          <Text className="text-slate-500">{isSignUp ? 'Already have an account?' : "Don't have an account?"}</Text>
          <Link href={isSignUp ? '/sign-in' : '/sign-up'} className="font-semibold text-indigo-600">
            {isSignUp ? 'Sign in' : 'Create one'}
          </Link>
        </View>
      </View>
    </ScrollView>
  );
}

export function AuthLoadingState() {
  return (
    <View className="flex-1 items-center justify-center bg-slate-50">
      <ActivityIndicator color="#4f46e5" size="large" />
    </View>
  );
}
