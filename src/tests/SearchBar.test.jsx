import { render, screen, fireEvent } from "@testing-library/react";
import SearchBar from "../components/SearchBar";

test("calls onSearch when user types in the input", () => {
  const mockOnSearch = jest.fn(); // mock function to track calls
  render(<SearchBar onSearch={mockOnSearch} />);

  const input = screen.getByPlaceholderText("Search...");

  fireEvent.change(input, { target: { value: "3D Printing Club" } });

  expect(mockOnSearch).toHaveBeenCalledWith("3D Printing Club");
});
