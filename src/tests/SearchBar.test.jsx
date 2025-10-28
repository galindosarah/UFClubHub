import { render, screen, fireEvent } from "@testing-library/react";
import SearchBar from "../components/SearchBar";

test("calls onSearch with input value when user types", () => {
  const mockOnSearch = jest.fn();
  render(<SearchBar onSearch={mockOnSearch} />);

  const input = screen.getByPlaceholderText("Search...");
  fireEvent.change(input, { target: { value: "3D Printing Club" } });

  // simulate pressing Enter
  fireEvent.keyDown(input, { key: "Enter", code: "Enter" });

  expect(mockOnSearch).toHaveBeenCalledWith("3D Printing Club");
});
