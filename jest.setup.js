import "@testing-library/jest-dom";

// Polyfill for TextEncoder/TextDecoder used by React Router
import { TextEncoder, TextDecoder } from "util";
if (!global.TextEncoder) global.TextEncoder = TextEncoder;
if (!global.TextDecoder) global.TextDecoder = TextDecoder;
