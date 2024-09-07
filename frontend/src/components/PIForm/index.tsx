import React from "react";
import { useForm } from "react-hook-form";
import "./index.css";

// Define the form's data structure
interface FormData {
  age: number;
  weight: number;
  height: number;
  sex: string;
  comments: string;
}

const PIForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();

  const onSubmit = (data: FormData) => {
    console.log(data); // Process the form data here
  };

  return (
    <div className="body">
      <h2 className="form__heading">Personalized Nutrient Plan</h2>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <div className="form__group">
          <label className="form__label" htmlFor="age">Age:</label>
          <input
            id="age"
            className="form__input"
            {...register("age", { required: true, min: 1 })}
          />
        </div>
        {errors.age && <p className="form__error">Age is required and should be a positive number.</p>}

        <div className="form__group">
          <label className="form__label" htmlFor="weight">Weight (kg):</label>
          <input
            id="weight"
            className="form__input"
            {...register("weight", { required: true, min: 1 })}
          />
        </div>
        {errors.weight && <p className="form__error">Weight is required and should be a positive number.</p>}

        <div className="form__group">
          <label className="form__label" htmlFor="height">Height (cm):</label>
          <input
            id="height"
            className="form__input"
            {...register("height", { required: true, min: 1 })}
          />
        </div>
        {errors.height && <p className="form__error">Height is required and should be a positive number.</p>}

        <div className="form__group">
          <label className="form__label" htmlFor="sex">Sex:</label>
          <select
            id="sex"
            className="form__select"
            {...register("sex", { required: true })}
          >
            <option value="">Select...</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        {errors.sex && <p className="form__error">Sex is required.</p>}

        {/* Comments Section */}
        <div className="form__group">
          <label className="form__label" htmlFor="comments">Comments:</label>
          <input
            id="comments"
            className="form__input"
            placeholder="Enter your comments..."
            {...register("comments")}
          />
        </div>

        <button className="form__button" type="submit">Get Nutrient Plan</button>
      </form>
    </div>
  );
};

export default PIForm;