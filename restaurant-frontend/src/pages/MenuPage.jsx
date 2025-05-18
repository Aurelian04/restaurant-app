import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function MenuPage() {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get('http://localhost:8000/api/menu/')
      .then(response => {
        console.log('API Response:', response.data);
        setDishes(response.data.results);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching menu:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container text-center my-5">
        <h2>Loading Menu...</h2>
      </div>
    );
  }

  return (
    <div className="container my-5">
      <h2 className="text-center mb-5">Our Menu</h2>
      <div className="row">
        {dishes.map(dish => (
          <div className="col-md-4 mb-4" key={dish.id}>
            <div className="card h-100 shadow-sm">
              <div className="card-body d-flex flex-column justify-content-between">
                <h5 className="card-title">{dish.name}</h5>
                <p className="card-text">{dish.description}</p>
                <p className="fw-bold">{dish.price} €</p>
                <button className="btn btn-primary mt-auto">Add to Cart</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MenuPage;
