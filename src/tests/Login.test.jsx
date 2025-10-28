import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import "@testing-library/jest-dom";
import Login from "../pages/Login";

const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

describe("Login Component", () => {
  beforeEach(() => {
    localStorage.clear();
    document.body.className = "";
    document.documentElement.className = "";
  });

  test("Error message when email is not a ufl.edu address", () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@gmail.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    expect(screen.getByText("Please use your @ufl.edu email address.")).toBeInTheDocument();
  });

  test("shows error when password is empty", () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@ufl.edu" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: " " },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));


    expect(screen.getByText("Password cannot be empty.")).toBeInTheDocument();
  });

  test("Navigates to /explore on successful login", () => {
    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "student@ufl.edu" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "securepassword" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));


    expect(mockNavigate).toHaveBeenCalledWith("/explore", { replace: true });
  });

});
