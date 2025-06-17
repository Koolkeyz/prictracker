import {
  Body,
  Container,
  Head,
  Heading,
  Html,
  Img,
  Link,
  Preview,
  Text,
  Tailwind,
  Button,
} from "@react-email/components";

interface ResetPasswordEmailProps {
  resetLink?: string;
  name?: string;
}

export const ResetPasswordEmail = ({
  resetLink,
  name,
}: ResetPasswordEmailProps) => (
  <Tailwind
    config={{
      theme: {
        extend: {
          colors: {},
        },
      },
    }}
  >
    <Html>
      <Head />
      <Preview>PriceTracker - Password Reset</Preview>
      <Body className="bg-gray-300">
        <Container className="mx-auto text-center">
          <Text className="text-2xl text-orange-500 font-semibold">
            PriceTracker
          </Text>
        </Container>

        <Container className="p-6 bg-white self-center max-w-md mx-auto rounded-2xl">
          <Heading className="text-2xl font-bold mb-4">
            Reset Your Password
          </Heading>
          <Text className="">Hi {'{{ name }}'},</Text>
          <Text className="mb-4">
            We received a request to reset your password. Click the button below
            to set a new password.
          </Text>
          <Container className="flex justify-center items-center w-full">
            <Button
              href="{{ resetLink }}"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mx-auto self-center text-center cursor-pointer w-96"
            >
              Reset Password
            </Button>
          </Container>
          <Text className="mt-3 text-gray-600">
            If you didn't request this, please ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  </Tailwind>
);

export default ResetPasswordEmail;
