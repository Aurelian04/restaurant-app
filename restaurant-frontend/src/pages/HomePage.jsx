import { Link } from 'react-router-dom';
import './HomePage.css'; // Importăm stiluri custom pentru background (creăm imediat fișierul)

function HomePage() {
  return (
    <div className="hero-section text-white d-flex align-items-center">
      <div className="container text-center">
        <h1 className="display-4 fw-bold mb-4">Welcome to Our Restaurant!</h1>
        <p className="lead mb-5">
          Discover delicious dishes made with passion and fresh ingredients. Your perfect dining experience awaits!
        </p>
        <div className="d-flex justify-content-center gap-3">
          <Link to="/menu" className="btn btn-primary btn-lg px-4">
            View Menu
          </Link>
          <Link to="/login" className="btn btn-outline-light btn-lg px-4">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
