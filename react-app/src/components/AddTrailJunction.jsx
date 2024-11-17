import React, { useState } from 'react';
import { useMutation } from '@apollo/client';
import { ADD_TRAIL_JUNCTION } from '../mutations';

const AddTrailJunction = () => {
  const [name, setName] = useState('');
  const [addTrailJunction, { data, loading, error }] = useMutation(ADD_TRAIL_JUNCTION);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addTrailJunction({ variables: { name } });
      setName('');  // Clear input after submission
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h3>Add a Trail Junction</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter junction name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button type="submit">Add</button>
      </form>
      {data && <p>Added Junction: {data.createTrailJunction.trailJunction.name}</p>}
    </div>
  );
};

export default AddTrailJunction;
