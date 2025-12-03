//import { useAuth } from "../context/AuthContext";
// import { Navigate } from "react-router-dom";

// export default function ProtectedRoute({ children, allowed }) {
//   const { userType } = useAuth();

//   if (!userType) {
//     return <Navigate to="/login" replace />;
//   }

//   if (!allowed.includes(userType)) {
//     return <Navigate to="/not-allowed" replace />;
//   }

//   return children;
// }

