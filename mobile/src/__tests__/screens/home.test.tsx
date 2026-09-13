import { render } from '@testing-library/react-native';

import HomeScreen from '@/app/index';

describe('<HomeScreen />', () => {
  test('Text renders correctly on HomeScreen', async () => {
    const { getByText } = await render(<HomeScreen />);

    getByText('Welcome!');
  });
});
